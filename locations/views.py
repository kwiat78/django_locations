import datetime

from django.db.models import Min, Max
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from locations.models import Location, Track
from locations.serializers import LocationSerializer, TrackSerializer, SimpleTrackSerializer


class LocationView(ModelViewSet):
    queryset = Location.objects.none()
    serializer_class = LocationSerializer

    def get_queryset(self):
        return Location.objects.filter(track__user=self.request.user).order_by("date")

    def create(self, request, *args, **kwargs):
        track = request.data.get('track')
        if track:
            Track.objects.get_or_create(label=track, user=request.user)
        return super(LocationView, self).create(request, *args, **kwargs)


class TrackViewSet(ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    lookup_field = 'label'
    lookup_url_kwarg = 'label'

    @staticmethod
    def _is_edited(label):
        return Location.objects.filter(edit=True, track__label=label).count() > 0

    def get_queryset(self):
        return Track.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        context = {
            "request": self.request,
        }
        serializer = SimpleTrackSerializer(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        return Response(self.get_queryset().values_list("label", flat=True), status=status.HTTP_200_OK)

    def retrieve(self, request, label=None):
        super().retrieve(request, label=label)
        criteria = {
            "track__label": label,
            "edit": TrackViewSet._is_edited(label)
        }
        last_date = request.query_params.get('last_date')
        if last_date:
            try:
                date = datetime.datetime.strptime(last_date, '%Y-%m-%dT%H:%M:%S.%fZ')
            except ValueError:
                date = datetime.datetime.strptime(last_date, '%Y-%m-%dT%H:%M:%SZ')

            criteria['date__gt'] = date

        queryset = Location.objects.filter(**criteria).order_by("position", "date")
        serializer = TrackSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, label=None):
        obj = get_object_or_404(self.get_queryset(), label=label)
        new_label = request.data.get("new_label", None)

        if not new_label:
            return Response("Specify new_label", status=status.HTTP_400_BAD_REQUEST)
        obj.label = new_label
        obj.save()
        return Response(status=status.HTTP_200_OK)

    def partial_update(self, request, label, *args, **kwargs):
        instance = self.get_object()
        serializer = SimpleTrackSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @detail_route()
    def params(self, request, label=None):
        obj = get_object_or_404(self.get_queryset(), label=label)
        res = {
            "points_number": obj.location_set.filter(edit=TrackViewSet._is_edited(label)).count(),
            "start_date": obj.location_set.aggregate(Min('date'))["date__min"],
            "stop_date": obj.location_set.aggregate(Max('date'))["date__max"],
            "processed": obj.processed,
            "ended": obj.ended
        }
        return Response(res, status=status.HTTP_200_OK)

    @list_route()
    def live(self, request):
        points = Location.objects.filter(track__ended=False).order_by('-date')
        if points:
            serializer = SimpleTrackSerializer(points[0].track)
            result = serializer.data
        else:
            result = ""
        return Response(result, status=status.HTTP_200_OK)

    @detail_route()
    def process(self, request, label=None):
        self.get_queryset().filter(label=label).update(processed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=["post"])
    def delete_edit(self, request, label=None):
        get_object_or_404(self.get_queryset(), label=label)
        Location.objects.filter(track__label=label, edit=True).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # TODO  decide what to do with the edited status
    @detail_route(methods=["post"])
    def join(self, request, label=None):
        track = get_object_or_404(self.get_queryset(), label=label)
        second_label = request.data.get("second_label", None)

        if not second_label:
            return Response("Needed second_label", status=status.HTTP_400_BAD_REQUEST)
        if label == second_label:
            return Response("Labels should be different", status=status.HTTP_400_BAD_REQUEST)

        second_track = get_object_or_404(self.get_queryset(), label=second_label)
        Location.objects.filter(track__label=second_label).update(track=track)
        second_track.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)