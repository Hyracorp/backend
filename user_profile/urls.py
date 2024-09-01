from django.urls import path
from .views import TenantUserProfileView,LandlordUserProfileView
urlpatterns = [
    path('tenant', TenantUserProfileView.as_view(), name='tenant-profile'),
    path('tenant/<int:id>', TenantUserProfileView.as_view(), name='tenant-profile'),
    path('landlord', LandlordUserProfileView.as_view(), name='landlord-profile'),
    path('landlord/<int:id>', LandlordUserProfileView.as_view(), name='landlord-profile'),
    path('id_proof', TenantUserProfileView.as_view(), name='id-proof'),
]
