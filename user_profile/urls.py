from django.urls import path
from .views import TenantUserProfileView
urlpatterns = [
    path('tenant', TenantUserProfileView.as_view(), name='tenant-profile'),
    path('tenant/<int:id>', TenantUserProfileView.as_view(), name='tenant-profile'),
]
