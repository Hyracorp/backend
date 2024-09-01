from rest_framework import serializers

from django.utils import timezone
from datetime import datetime, timedelta


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
        fields = ["id", "name", "icon"]


class PropertyPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyPhoto
        fields = ["id", "photo_url", "alt_text", "title", "approved"]
        extra_kwargs = {
            # If you don't want users to set this field directly
            'approved': {'read_only': True},
        }

    def validate_photo_url(self, value):
        """
        Optional: Validate the photo URL if needed.
        """
        if not value:
            raise serializers.ValidationError("Photo URL cannot be empty.")
        return value

    def validate(self, data):
        """
        Optional: Add any additional validation logic here.
        """
        if not data.get('alt_text'):
            raise serializers.ValidationError("Alt text is required.")
        if not data.get('title'):
            raise serializers.ValidationError("Title is required.")
        return data


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
        fields = ["id", "title", "city", "state", "pincode",
                  "bhk", "expected_rate_rent", "first_photo_url"]

    def get_first_photo_url(self, obj):
        try:
            return obj.photos.first().photo_url.url
        except:
            return None


class CommercialPropertySearchSerializer(serializers.ModelSerializer):
    first_photo_url = serializers.SerializerMethodField()

    class Meta(BasePropertySerializer.Meta):
        model = CommercialProperty
        fields = ["id", "title", "city", "state", "pincode",
                  "expected_rate_rent", "first_photo_url"]

    def get_first_photo_url(self, obj):
        try:
            return obj.photos.first().photo_url.url
        except:
            return None


class BookVisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookVisit
        fields = '__all__'
        extra_kwargs = {
            'visit_status': {'required': True},
            'phone': {'required': True},
            'gender': {'required': True},
            # Mark visit_status as optional
            'visit_status': {'required': False},
            'user': {'read_only': True},  # Mark user as optional
        }

    def validate(self, data):
        """
        Ensure the booking meets time constraints and slot availability.
        """
        now = timezone.localtime(
            timezone.now())  # This is timezone-aware and uses the local timezone

        # Combine date and time, and make it timezone-aware
        booking_naive = datetime.combine(
            data['date'], datetime.strptime(data['time'], "%H:%M").time())
        booking_datetime = timezone.make_aware(
            booking_naive, timezone.get_current_timezone())

        # Ensure the booking is made at least 5 hours in advance
        if booking_datetime - now < timedelta(hours=5):
            raise serializers.ValidationError(
                "You must book a visit at least 5 hours in advance.")

        # Check that the time slot is available
        if BookVisit.objects.filter(
            property=data['property'],
            date=data['date'],
            time=data['time']
        ).exists():
            raise serializers.ValidationError(
                "This time slot is already booked.")

        return data

    def create(self, validated_data):
        """
        Automatically set visit_status to "Pending" and assign the current user to the booking.
        """
        validated_data['visit_status'] = "Pending"
        validated_data['user'] = self.context['request'].user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Handle approval logic when updating the visit status.
        """
        if 'visit_status' in validated_data:
            if validated_data['visit_status'] == 'Approved' and instance.visit_status != 'Pending':
                raise serializers.ValidationError(
                    "Visit can only be approved if it is in Pending status.")

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """
        Automatically mark visit_status as 'Expired' if the booking date has passed and status is not 'Finalized' or 'Visited'.
        """
        now = timezone.localtime(timezone.now())

        # Combine the booking date and time, and make it timezone-aware
        booking_naive = datetime.combine(
            instance.date, datetime.strptime(instance.time, "%H:%M").time())
        booking_datetime = timezone.make_aware(
            booking_naive, timezone.get_current_timezone())

        # Check if the booking date has passed
        if booking_datetime < now:
            if instance.visit_status not in ['Finalized', 'Visited']:
                # Update the status to 'Expired' if it hasn't already been set
                instance.visit_status = 'Expired'
                instance.save()

        return super().to_representation(instance)
