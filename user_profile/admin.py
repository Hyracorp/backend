from django.contrib import admin

from .models import TenantUserProfile, LandlordUserProfile

# Register your models here.
admin.site.register(TenantUserProfile, LandlordUserProfile)
