from __future__ import annotations

from rest_framework import serializers

from ruian.data.models import City, OrpEntity, PouEntity


class PouEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PouEntity
        fields = [
            "code",
            "name",
        ]


class OrpEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrpEntity
        fields = [
            "code",
            "name",
        ]


class CitySerializer(serializers.ModelSerializer):
    pou = PouEntitySerializer(many=False)
    orp = OrpEntitySerializer(many=False)

    class Meta:
        model = City
        fields = [
            "code",
            "name",
            "pou",
            "orp",
        ]
