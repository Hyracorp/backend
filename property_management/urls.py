from django.urls import path
from .views import PropertyView, PropertyDetailView, PropertySearchView, AvailableSlotsAPIView, BookVisitAPIView, UpdateVisitStatusAPIView, FeaturedPropertyView,BookVisitListAPIView,AmenitiesView,PropertyPhotoView
urlpatterns = [

    path("search", PropertySearchView.as_view()),
    path("", PropertyView.as_view()),
    path("<int:pk>", PropertyDetailView.as_view()),
    path("photos", PropertyPhotoView.as_view({'post': 'create'})),
    path("photos/<int:pk>", PropertyPhotoView.as_view({'patch': 'partial_update'})),
    path("booking/slots", AvailableSlotsAPIView.as_view()),
    path("booking", BookVisitAPIView.as_view()),
    path("booking/list", BookVisitListAPIView.as_view()),
    path("booking/<int:pk>", UpdateVisitStatusAPIView.as_view()),
    path("featured", FeaturedPropertyView.as_view()),
    path("amenities", AmenitiesView.as_view()),

]
