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


class IsLandlordOrTenantReadOnly(permissions.BasePermission):
    """
    Custom permission to allow:
    - Landlords to perform any CRUD operation, but only on properties they own.
    - Tenants to view properties (read-only).
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Allow full access for landlords
            if request.user.is_landlord:
                return True
            
            # Allow read-only access for tenants (non-landlords)
            if request.user.is_tenant and request.method in permissions.SAFE_METHODS:
                return True
            
            # Deny modification access for tenants
            return False

        # If user is not authenticated, deny access
        return False

    def has_object_permission(self, request, view, obj):
        # Allow full access for landlords, but only on their own properties
        if request.user.is_landlord:
            return obj.user == request.user  # Only allow actions on their own properties

        # Allow read-only access for tenants
        if request.user.is_tenant and request.method in permissions.SAFE_METHODS:
            return True

        # Deny all other cases
        return False

