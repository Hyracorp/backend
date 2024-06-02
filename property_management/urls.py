from django.urls import path

from .views import ResidentialPropertyView

urlpatterns = [
    path("property", ResidentialPropertyView.as_view(), name="property"),
    path("property/<int:id>", ResidentialPropertyView.as_view(), name="property"),
]
