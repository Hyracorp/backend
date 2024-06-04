from django.contrib import admin
from .models import TenantUserProfile, LandlordUserProfile

admin.site.register(TenantUserProfile)
admin.site.register(LandlordUserProfile)
