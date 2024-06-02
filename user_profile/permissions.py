from rest_framework import permissions
from user_auth.models import User


class IsTenantUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        print(user.id)
        try:
            tenant_profile = User.objects.get(id=user.id)
        except User.DoesNotExist:
            return False
        if tenant_profile.is_tenant is True:
            return True
        return False


class IsLandlordUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            landlord_profile = User.objects.get(id=user.id)
        except User.DoesNotExist:
            return False
        if landlord_profile.is_landlord is True:
            return True
        return False
