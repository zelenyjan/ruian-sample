from __future__ import annotations

from django.db import models


class CodeNameEntity(models.Model):
    code = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name


class PouEntity(CodeNameEntity):
    class Meta:
        verbose_name = "POU"
        verbose_name_plural = "POU"


class OrpEntity(CodeNameEntity):
    class Meta:
        verbose_name = "ORP"
        verbose_name_plural = "ORP"


class Region(CodeNameEntity):
    class Meta:
        verbose_name = "kraj"
        verbose_name_plural = "kraje"


class District(CodeNameEntity):
    region = models.ForeignKey(Region, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "okres"
        verbose_name_plural = "okresy"


class City(CodeNameEntity):
    pou = models.ForeignKey(PouEntity, on_delete=models.PROTECT)
    orp = models.ForeignKey(OrpEntity, on_delete=models.PROTECT)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name = "obec"
        verbose_name_plural = "obce"

    def __str__(self) -> str:
        return self.name


class CityCodeNameEntity(CodeNameEntity):
    city = models.ForeignKey(City, on_delete=models.PROTECT)

    class Meta:
        abstract = True


class CityPart(CityCodeNameEntity):
    class Meta:
        verbose_name = "část obce"
        verbose_name_plural = "části obce"


class CityArea(CityCodeNameEntity):
    class Meta:
        verbose_name = "dělení obcí"
        verbose_name_plural = "dělení obcí"


class Street(CityCodeNameEntity):
    class Meta:
        verbose_name = "ulice"
        verbose_name_plural = "ulice"


class Place(models.Model):
    code = models.PositiveIntegerField(primary_key=True, verbose_name="RUIAN")
    conscription_number = models.CharField(max_length=64, default="")
    street_number = models.CharField(max_length=64, default="")
    provisional_number = models.CharField(max_length=64, default="")
    zip_number = models.PositiveIntegerField()

    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    city_part = models.ForeignKey(CityPart, on_delete=models.PROTECT, null=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    street = models.ForeignKey(Street, on_delete=models.PROTECT, null=True)

    city_area1 = models.ForeignKey(CityArea, on_delete=models.PROTECT, related_name="+", null=True)
    city_area2 = models.ForeignKey(CityArea, on_delete=models.PROTECT, related_name="+", null=True)
    city_area3 = models.ForeignKey(CityArea, on_delete=models.PROTECT, related_name="+", null=True)

    raw_data = models.JSONField()

    class Meta:
        verbose_name = "adresa"
        verbose_name_plural = "adresy"

    def __str__(self) -> str:
        return self.raw_data["FORMATTED_ADDRESS_WHOLE"]
