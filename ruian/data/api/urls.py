from __future__ import annotations

from rest_framework import routers

from .views import CityViewSet, PlaceViewSet

app_name = "data_api"

router = routers.SimpleRouter()
router.register("city", CityViewSet, basename="city")
router.register("place", PlaceViewSet, basename="place")
urlpatterns = router.urls
