from django.urls import path

from .views import ResidentialPropertyView, BookVisitView

urlpatterns = [
    path("<int:id>", ResidentialPropertyView.as_view(), name="property"),
    path("book", BookVisitView.as_view(), name="property-book-visit"),
]
