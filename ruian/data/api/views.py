from __future__ import annotations

from rest_framework import decorators, mixins, status, viewsets
from rest_framework.response import Response

from requests import HTTPError
from ruian.data.api.serializers import CitySerializer
from ruian.data.cuzk import get_data_from_cuzk_and_create_city_instance
from ruian.data.models import (
    City,
    CityArea,
    CityPart,
    CodeNameEntity,
    Place,
    Region,
    Street,
)


class CityViewSet(viewsets.GenericViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    @decorators.action(detail=True, methods=["GET"])
    def get_or_create_city(self, request, pk):
        try:
            city = City.objects.get(pk=pk)
        except City.DoesNotExist:
            try:
                city = get_data_from_cuzk_and_create_city_instance(pk)
            except HTTPError:
                return Response({"error": "Request error"}, status=status.HTTP_424_FAILED_DEPENDENCY)
        return Response(CitySerializer(instance=city).data)


class PlaceViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Place.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        raw_data = data["address_data"]

        # get city
        try:
            city = City.objects.get(pk=raw_data["CITY_CODE"])
        except City.DoesNotExist:
            try:
                city = get_data_from_cuzk_and_create_city_instance(raw_data["CITY_CODE"])
            except HTTPError:
                return Response({"error": "Request error"}, status=status.HTTP_424_FAILED_DEPENDENCY)

        def get_instance(
            base_key: str, klass: type[CodeNameEntity], extra_defaults: dict | None = None
        ) -> CodeNameEntity | None:
            if code := raw_data[f"{base_key.upper()}_CODE"]:
                update_defaults = {
                    "name": raw_data[base_key.upper()],
                }

                if extra_defaults:
                    update_defaults |= extra_defaults

                obj, _ = klass.objects.update_or_create(
                    code=code,
                    defaults=update_defaults,
                )
                return obj
            else:
                return None

        defaults = {
            "conscription_number": raw_data["CONSCRIPTION_NUMBER"],
            "street_number": raw_data["STREET_NUMBER"],
            "provisional_number": raw_data["PROVISIONAL_NUMBER"],
            "zip_number": raw_data["ZIP"],
            "district": city.district,
            "city": city,
            "city_part": get_instance("PART", CityPart, {"city": city}),
            "region": get_instance("REGION", Region),
            "street": get_instance("STREET", Street, {"city": city}),
            "city_area1": get_instance("CITY_AREA_1", CityArea, {"city": city}),
            "city_area2": get_instance("CITY_AREA_2", CityArea, {"city": city}),
            "city_area3": get_instance("CITY_AREA_3", CityArea, {"city": city}),
            "raw_data": raw_data,
        }

        place, _ = Place.objects.update_or_create(
            code=raw_data["CODE"],
            defaults=defaults,
        )

        return Response({"success": True})
