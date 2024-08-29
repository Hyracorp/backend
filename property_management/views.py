
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ResidentialProperty, CommercialProperty, BaseProperty
from .serializers import ResidentialPropertySerializer, CommercialPropertySerializer, BasePropertySerializer, ResidentialPropertySearchSerializer, CommercialPropertySearchSerializer
from rest_framework.permissions import IsAuthenticated
from user_profile.permissions import IsLandlordOrTenantReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

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
    def get_queryset(self):
        property_type = self.request.query_params.get('property_type')
        if property_type == 'Commercial':
            return CommercialProperty.objects.filter(approved=True)
        elif property_type == 'Residential':
            return ResidentialProperty.objects.filter(approved=True)
        else:
            raise Http404("Property type not found or invalid.")

    def get_serializer_class(self):
        property_type = self.request.query_params.get('property_type')
        if property_type == 'Residential':
            return ResidentialPropertySearchSerializer 
        elif property_type == 'Commercial':
            return CommercialPropertySearchSerializer
        return BasePropertySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['property_type', 'service_type','city']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['property_type'] = self.request.query_params.get('property_type')
        return context


