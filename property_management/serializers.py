from rest_framework import serializers

from .models import (
    ResidentialProperty,
    CommercialProperty,
    PropertyPhoto,
    Amenity,
    BookVisit,
)


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["id", "name"]


class PropertyPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyPhoto
        fields = ["id", "photo_url"]


class ResidentialPropertySerializer(serializers.ModelSerializer):
    photos = PropertyPhotoSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)

    class Meta:
        model = ResidentialProperty
        fields = "__all__"


class CommercialPropertySerializer(serializers.ModelSerializer):
    photos = PropertyPhotoSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)

    class Meta:
        model = CommercialProperty
        fields = "__all__"


class BookVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookVisit
        fields = "__all__"
