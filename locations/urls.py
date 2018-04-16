from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from locations.views import LocationView, TrackViewSet

router = DefaultRouter()
router.register(r"locations", LocationView, base_name="locations")
router.register(r"tracks", TrackViewSet, base_name="tracks")

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^feeds/(?P<feed>[^/.]+)/', include(router.urls)),
]