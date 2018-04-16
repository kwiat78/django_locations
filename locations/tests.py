from datetime import datetime
import pytz
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from locations.models import Location, Track


class TrackTests(TestCase):
    fixtures = ['tracks']

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(username='user1')
        self.client.force_authenticate(self.user)
        self.URL_TRACKS = reverse("tracks-list")

    def test_get_tracks(self):
        result = self.client.get(self.URL_TRACKS, format='json')
        assert result.status_code == status.HTTP_200_OK
        assert len(result.data) == 2
        assert "Track_1" in result.data
        assert "Track_2" in result.data

    def test_create_track(self):
        result = self.client.post(self.URL_TRACKS, data={"label": "Track_3"}, format='json')
        assert result.status_code == status.HTTP_201_CREATED
        assert result.data["label"] == "Track_3"
        assert Track.objects.count() == 3

    def test_get_track_params(self):
        result = self.client.get(reverse("tracks-params", args=("Track_2",)), format='json')
        assert result.status_code == status.HTTP_200_OK
        assert result.data["points_number"] == 3
        assert result.data["processed"] == False
        assert result.data["ended"] == True
        assert result.data["start_date"] == datetime(2018, 2, 20, 13, tzinfo=pytz.UTC)
        assert result.data["stop_date"] == datetime(2018, 2, 20, 13, 1, tzinfo=pytz.UTC)

    def test_get_track_process(self):
        result = self.client.get(reverse("tracks-process", args=("Track_2",)), format='json')
        assert result.status_code == status.HTTP_204_NO_CONTENT
        assert Track.objects.get(label='Track_2').processed

    def test_change_name(self):
        result = self.client.put(reverse("tracks-detail", args=("Track_2",)), data={"new_label": "T2.1"}, format='json')
        assert result.status_code == status.HTTP_200_OK
        assert Track.objects.filter(label='T2.1').exists()

    def test_join_tracks(self):
        result = self.client.post(
            reverse("tracks-join", args=("Track_1",)),
            data={"second_label": "Track_2"},
            format='json'
        )
        assert result.status_code == status.HTTP_204_NO_CONTENT
        assert Track.objects.count() == 1
        assert Location.objects.filter(track__label='Track_1').count() == 8

    def test_get_track(self):
        result = self.client.get(reverse("tracks-detail", args=("Track_1",)), format='json')
        assert result.status_code == status.HTTP_200_OK
        assert len(result.data) == 3

    def test_get_track_older_locations(self):
        result = self.client.get(
            reverse("tracks-detail", args=("Track_1",)),
            data={"last_date": "2018-02-20T12:00:59Z"},
            format='json'
        )
        assert result.status_code == status.HTTP_200_OK
        assert len(result.data) == 2

    def test_delete_edit(self):
        result = self.client.post(reverse("tracks-delete-edit", args=("Track_2",)), format='json')
        assert result.status_code == status.HTTP_204_NO_CONTENT
        assert Track.objects.count() == 2
        assert Location.objects.filter(track__label='Track_2').count() == 2
        assert Location.objects.filter(track__label='Track_2', edit=True).count() == 0

    def test_no_live_track(self):
        result = self.client.get(reverse("tracks-live", ), format='json')
        assert result.status_code == status.HTTP_200_OK
        assert result.data == ""

    def test_live_track(self):
        track = Track.objects.create(label="Track3", user=self.user)
        Location.objects.create(latitude="0.01", longitude="0.02", track=track)
        result = self.client.get(reverse("tracks-live", ), format='json')
        assert result.status_code == status.HTTP_200_OK
        assert result.data["label"] == "Track3"
        assert result.data["ended"] == False


class LocationTests(TestCase):
    fixtures = ['tracks']

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(username='user1')
        self.client.force_authenticate(self.user)
        self.URL_LOCATIONS = reverse("locations-list")

    def test_post_location_existing_track(self):
        result = self.client.post(
            self.URL_LOCATIONS,
            data={
                "latitude": "0.1",
                "longitude": "0.1",
                "track": "Track_1",
                "position": 3,
            },
            format='json'
        )
        assert result.status_code == status.HTTP_201_CREATED
        assert result.data["latitude"] == 0.1
        assert result.data["longitude"] == 0.1
        assert result.data["edit"] == False
        assert Location.objects.filter(track__label='Track_1').count() == 4

    def test_post_location_new_track(self):
        result = self.client.post(
            self.URL_LOCATIONS,
            data={
                "latitude": "0.1",
                "longitude": "0.1",
                "track": "Track_3",
                "position": 0,
            },
            format='json'
        )
        assert result.status_code == status.HTTP_201_CREATED
        assert result.data["latitude"] == 0.1
        assert result.data["longitude"] == 0.1
        assert result.data["edit"] == False
        assert Track.objects.filter(label='Track_3').exists()
        assert Location.objects.filter(track__label='Track_3').count() == 1
