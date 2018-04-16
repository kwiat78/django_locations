from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, SlugRelatedField, HiddenField, CurrentUserDefault

from locations.models import Location, Track


class LocationSerializer(ModelSerializer):

    track = SlugRelatedField(slug_field="label", queryset=Track.objects.all())

    class Meta:
        model = Location
        fields = ("latitude", "longitude", "date", "track", "position", "edit")


class TrackSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = ('latitude', 'longitude', 'date')


class SimpleTrackSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Track
        fields = ('label', 'user', 'ended')
