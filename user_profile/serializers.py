from rest_framework import serializers
from user_auth.models import User

from .models import TenantUserProfile, LandlordUserProfile


class TenantUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantUserProfile
        fields = "__all__"
        extra_kwargs = {"user": {"required": False}}

    def validate(self, attrs):
        try:
            user = User.objects.get(id=attrs["user"].id)
            if user.is_active is True:
                if not user.is_tenant:
                    raise serializers.ValidationError("User is not a tenant")
                else:
                    return attrs
            else:
                raise serializers.ValidationError("User is not active")
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")
        return attrs


class LandlordUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandlordUserProfile
        fields = "__all__"
        extra_kwargs = {"user": {"required": False}}

    def validate(self, attrs):
        try:
            user = User.objects.get(id=attrs["user"].id)
            if user.is_active is True:
                if not user.is_landlord:
                    raise serializers.ValidationError("User is not a tenant")
                else:
                    return attrs
            else:
                raise serializers.ValidationError("User is not active")
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")
        return attrs
