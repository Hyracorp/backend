from django.urls import path

from .views import ResidentialPropertyView, BookVisitView, CommercialPropertyView

urlpatterns = [
    path("residential", ResidentialPropertyView.as_view()),
    path("residential/<int:id>", ResidentialPropertyView.as_view()),
    path("commercial", CommercialPropertyView.as_view()),
    path("commercial/<int:id>", CommercialPropertyView.as_view()),
    path("book", BookVisitView.as_view()),
]
