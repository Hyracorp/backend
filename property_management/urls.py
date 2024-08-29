from django.urls import path
from .views import  PropertyView, PropertyDetailView, PropertySearchView
urlpatterns = [
 
    path("search", PropertySearchView.as_view()),
    path("",PropertyView.as_view()),
    path("<int:pk>", PropertyDetailView.as_view()),
]
