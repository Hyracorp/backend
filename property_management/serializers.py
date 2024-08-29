from rest_framework import serializers

from .models import (
    ResidentialProperty,
    CommercialProperty,
    PropertyPhoto,
    Amenity,
    BookVisit,
    BaseProperty
)

class BasePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseProperty
        fields = '__all__'
class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["id", "name"]


class PropertyPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyPhoto
        fields = ["id", "photo_url"]


class ResidentialPropertySerializer(BasePropertySerializer):
    photos = PropertyPhotoSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)

    class Meta(BasePropertySerializer.Meta):
        model = ResidentialProperty
        fields = "__all__"


class CommercialPropertySerializer(BasePropertySerializer):
    photos = PropertyPhotoSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)

    class Meta(BasePropertySerializer.Meta):
        model = CommercialProperty
        fields = "__all__"

class ResidentialPropertySearchSerializer(serializers.ModelSerializer):
    first_photo_url = serializers.SerializerMethodField()
    class Meta(BasePropertySerializer.Meta):
        model = ResidentialProperty
        fields = ["id","title", "city", "state", "pincode","bhk","expected_rate_rent","first_photo_url"]

    def get_first_photo_url(self, obj):
        try:
            return obj.photos.first().photo_url.url
        except:
            return None

class CommercialPropertySearchSerializer(serializers.ModelSerializer):
    first_photo_url = serializers.SerializerMethodField()
    class Meta(BasePropertySerializer.Meta):
        model = CommercialProperty
        fields = ["id","title", "city", "state", "pincode","expected_rate_rent","first_photo_url"]
    def get_first_photo_url(self, obj):
        try:
            return obj.photos.first().photo_url.url
        except:
            return None
class BookVisitSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BookVisit
        fields = "__all__"
