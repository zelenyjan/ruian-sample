from __future__ import annotations

from django.contrib import admin

from ruian.data.models import (
    City,
    CityArea,
    CityPart,
    District,
    OrpEntity,
    Place,
    PouEntity,
    Region,
    Street,
)


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    pass


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    pass


@admin.register(CityArea)
class CityAreaAdmin(admin.ModelAdmin):
    pass


@admin.register(CityPart)
class CityPartAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    pass


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(OrpEntity)
class OrpEntityAdmin(admin.ModelAdmin):
    pass


@admin.register(PouEntity)
class PouEntityAdmin(admin.ModelAdmin):
    pass
