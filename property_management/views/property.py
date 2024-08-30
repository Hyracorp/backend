
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from property_management.models import ResidentialProperty, CommercialProperty, BaseProperty
from property_management.serializers import ResidentialPropertySerializer, CommercialPropertySerializer, BasePropertySerializer, ResidentialPropertySearchSerializer, CommercialPropertySearchSerializer
from rest_framework.permissions import IsAuthenticated
from user_profile.permissions import IsLandlordOrTenantReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist, ValidationError

#Proximity Search

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
    queryset = queryset.annotate(distance=distance_expr).filter(distance__lte=max_distance)
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
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        property_type = request.data.get('property_type')

        if property_type == 'Residential':
            serializer = ResidentialPropertySerializer(data=request.data)
        elif property_type == 'Commercial':
            serializer = CommercialPropertySerializer(data=request.data)
        else:
            return Response({"error": "Invalid property_type provided."}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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

        try:
            serializer = serializer_class(instance, data=request.data, partial=partial)
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
        max_distance = self.request.query_params.get('max_distance', 10)  # Default to 10 km

        # Validate property type
        if property_type not in ['Commercial', 'Residential']:
            raise ValidationError({"property_type": "Invalid or missing property_type. Must be 'Commercial' or 'Residential'."})

        # Get the appropriate queryset based on property type
        if property_type == 'Commercial':
            queryset = CommercialProperty.objects.filter(approved=True)
        elif property_type == 'Residential':
            queryset = ResidentialProperty.objects.filter(approved=True)
        
        # If latitude and longitude are provided, filter by proximity
        if lat and lon:
            try:
                lat = float(lat)
                lon = float(lon)
                max_distance = float(max_distance)
            except ValueError:
                raise ValidationError({"latitude/longitude/max_distance": "Invalid format. These should be valid float numbers."})
            
            queryset = filter_properties_by_proximity(queryset, lat, lon, max_distance)
        elif lat or lon:
            # If one of the coordinates is missing
            raise ValidationError({"latitude/longitude": "Both latitude and longitude must be provided together."})

        return queryset

    def get_serializer_class(self):
        property_type = self.request.query_params.get('property_type')
        if property_type == 'Residential':
            return ResidentialPropertySearchSerializer
        elif property_type == 'Commercial':
            return CommercialPropertySearchSerializer
        return BasePropertySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['property_type'] = self.request.query_params.get('property_type')
        return context
