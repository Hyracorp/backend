
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from property_management.models import ResidentialProperty, CommercialProperty, BaseProperty, BookVisit, PropertyPhoto, Amenity
from property_management.serializers import ResidentialPropertySerializer, CommercialPropertySerializer, BasePropertySerializer, ResidentialPropertySearchSerializer, CommercialPropertySearchSerializer, BookVisitSerializer, PropertyPhotoSerializer, BasePropertySearchSerializer, BasePropertyListSerializer, AmenitySerializer
from rest_framework.permissions import IsAuthenticated
from user_profile.permissions import IsLandlordOrTenantReadOnly, NewIsLandlordOrTenantReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import get_object_or_404
# Proximity Search

import math
from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models.functions import ACos, Cos, Radians, Sin


def filter_properties_by_proximity(queryset, target_lat, target_lon, max_distance):
    """
    Filters properties by proximity to the target latitude and longitude using the Haversine formula.
    """
    # Convert degrees to radians
    target_lat_rad = Radians(target_lat)
    target_lon_rad = Radians(target_lon)

    # Haversine formula
    distance_expr = ExpressionWrapper(
        6371 * ACos(
            Cos(Radians(F('latitude'))) * Cos(target_lat_rad) *
            Cos(Radians(F('longitude')) - target_lon_rad) +
            Sin(Radians(F('latitude'))) * Sin(target_lat_rad)
        ),
        output_field=FloatField()
    )

    # Annotate the queryset with the calculated distance and filter by max_distance
    queryset = queryset.annotate(distance=distance_expr).filter(
        distance__lte=max_distance)
    return queryset


# view or add property
class PropertyView(APIView):
    permission_classes = [IsAuthenticated, IsLandlordOrTenantReadOnly]

    def get(self, request, pk=None):
        if pk is not None:
            try:
                property = BaseProperty.objects.get(pk=pk)
            except BaseProperty.DoesNotExist:
                raise Http404("Property not found.")

            if property.property_type == "Residential":
                try:
                    property = ResidentialProperty.objects.get(pk=pk)
                except ResidentialProperty.DoesNotExist:
                    raise Http404("Residential Property not found.")
                serializer = ResidentialPropertySerializer(property)
            elif property.property_type == "Commercial":
                try:
                    property = CommercialProperty.objects.get(pk=pk)
                except CommercialProperty.DoesNotExist:
                    raise Http404("Commercial Property not found.")
                serializer = CommercialPropertySerializer(property)
            else:
                serializer = BasePropertySerializer(property)
            return Response(serializer.data)
        else:
            try:
                if request.user.is_superuser:
                    queryset = BaseProperty.objects.all()
                elif request.user.is_landlord:
                    queryset = BaseProperty.objects.filter(user=request.user)
                else:
                    queryset = BaseProperty.objects.none()
                serializer = BasePropertyListSerializer(queryset, many=True)
                return Response(serializer.data)
            except BaseProperty.DoesNotExist:
                return Response({"error": "No properties found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        property_type = request.data.get('property_type')

        # Create a mutable copy of the request data
        data = request.data.copy()
        data["user"] = request.user.id  # Attach the user to the data

        # Define the BHK choices mapping
        BHK_CHOICES = {
            "1 BHK": 1,
            "2 BHK": 2,
            "3 BHK": 3,
            "4 BHK": 4,
        }

        # Check if it's a Residential property and adjust the BHK value if needed
        if property_type == 'Residential' and data.get("bhk") in BHK_CHOICES.keys():
            # Convert the string value to an integer
            data["bhk"] = int(BHK_CHOICES[data["bhk"]])

        # Choose the correct serializer based on the property type
        if property_type == 'Residential':
            serializer = ResidentialPropertySerializer(data=data)
        elif property_type == 'Commercial':
            serializer = CommercialPropertySerializer(data=data)
        else:
            return Response({"error": "Invalid property_type provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate and save the data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Return validation errors if any
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# view, update or delete property

class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsLandlordOrTenantReadOnly]
    queryset = BaseProperty.objects.all()

    def get_object(self):
        try:
            obj = super().get_object()
        except ObjectDoesNotExist:
            raise Http404("Property not found.")

        if obj.property_type == "Residential":
            try:
                return ResidentialProperty.objects.get(pk=obj.pk)
            except ResidentialProperty.DoesNotExist:
                raise Http404("Residential Property not found.")
        elif obj.property_type == "Commercial":
            try:
                return CommercialProperty.objects.get(pk=obj.pk)
            except CommercialProperty.DoesNotExist:
                raise Http404("Commercial Property not found.")
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Get the serialized data
        data = serializer.data

        # Add booking information
        user = request.user
        bookings = BookVisit.objects.filter(property=instance, user=user)
        booking_data = BookVisitSerializer(bookings, many=True).data

        # Add the booking data to the response
        data['bookings'] = booking_data

        return Response(data)

    def get_serializer_class(self):

        instance = self.get_object()
        if isinstance(instance, ResidentialProperty):
            return ResidentialPropertySerializer
        elif isinstance(instance, CommercialProperty):
            return CommercialPropertySerializer
        return BasePropertySerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer_class = self.get_serializer_class()
        user = request.user.id
        data = request.data
        data['user'] = user

        try:
            serializer = serializer_class(
                instance, data=data, partial=partial)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

# search property


class PropertySearchView(generics.ListAPIView):
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['property_type', 'service_type', 'city']

    def get_queryset(self):
        # Get query parameters
        property_type = self.request.query_params.get('property_type')
        lat = self.request.query_params.get('latitude')
        lon = self.request.query_params.get('longitude')
        max_distance = self.request.query_params.get(
            'max_distance', 10)  # Default to 10 km

        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        bhk = self.request.query_params.getlist('bhk')

        # Validate property type
        if property_type not in ['Commercial', 'Residential']:
            return Response(
                {"error": "Invalid or missing property_type. Must be 'Commercial' or 'Residential'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get the appropriate queryset based on property type
        if property_type == 'Commercial':
            queryset = CommercialProperty.objects.filter(approved=True)
        elif property_type == 'Residential':
            queryset = ResidentialProperty.objects.filter(approved=True)

        # If min_price and max_price are provided, filter by price
        if min_price or max_price:
            try:
                if min_price:
                    min_price = float(min_price)
                    queryset = queryset.filter(
                        expected_rate_rent__gte=min_price)
                if max_price:
                    max_price = float(max_price)
                    queryset = queryset.filter(
                        expected_rate_rent__lte=max_price)
            except ValueError:
                return Response(
                    {"error": "Invalid format for min_price or max_price. These should be valid float numbers."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        if bhk and property_type == 'Residential':
            try:
                bhk = [int(b) for b in bhk]  # Convert to integers
                if 4 in bhk:
                    queryset = queryset.filter(bhk__gte=4)
                else:
                    queryset = queryset.filter(bhk__in=bhk)
            except ValueError:
                return Response(
                    {"error": "Invalid format for bhk. It should be a list of integers."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        # If latitude and longitude are provided, filter by proximity
        if lat and lon:
            try:
                lat = float(lat)
                lon = float(lon)
                max_distance = float(max_distance)
            except ValueError:
                return Response(
                    {"error": "Invalid format for latitude, longitude, or max_distance. These should be valid float numbers."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            queryset = filter_properties_by_proximity(
                queryset, lat, lon, max_distance)
        elif lat or lon:
            # If one of the coordinates is missing
            return Response(
                {"error": "Both latitude and longitude must be provided together."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return queryset

    def list(self, request, *args, **kwargs):
        # Override the list method to handle the Response object from get_queryset
        queryset = self.get_queryset()

        # If the queryset is actually a Response object, return it directly
        if isinstance(queryset, Response):
            return queryset

        # Continue with the normal flow if queryset is valid
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        property_type = self.request.query_params.get('property_type')
        if property_type == 'Residential':
            return ResidentialPropertySearchSerializer
        elif property_type == 'Commercial':
            return CommercialPropertySearchSerializer
        return BasePropertySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['property_type'] = self.request.query_params.get(
            'property_type')
        return context


class PropertyPhotoView(viewsets.ModelViewSet):
    queryset = PropertyPhoto.objects.all()
    serializer_class = PropertyPhotoSerializer
    permission_classes = [IsAuthenticated, NewIsLandlordOrTenantReadOnly]

    def perform_create(self, serializer):
        # Get the 'property' field from form data
        property_id = self.request.POST.get('property')

        # Ensure the property exists, or return 404 if not found
        property_instance = get_object_or_404(BaseProperty, id=property_id)

        # Get the uploaded file from form data (usually under request.FILES)
        photo_file = self.request.FILES.get('photo_url')

        # Get the 'title' field from the form data
        title = self.request.POST.get('title')

        # Create a dictionary to pass data to the serializer
        data = {
            'photo_url': photo_file,  # File is handled by request.FILES
            'title': title,
        }

        # If you have additional fields, add them to the data dictionary

        # Validate and save the serializer
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            # Save the PropertyPhoto instance and associate it with the property
            serializer.save(property=property_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        # Handle file upload and form data in POST request
        return self.perform_create(self.get_serializer())


class FeaturedPropertyView(generics.ListAPIView):
    permission_classes = []
    serializer_class = BasePropertySearchSerializer

    def get_queryset(self):
        # Return the first 3 properties
        return BaseProperty.objects.all()[:3]


class AmenitiesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AmenitySerializer
    queryset = Amenity.objects.all()
    pagination_class = None
