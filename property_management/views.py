from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user_profile.permissions import IsLandlordUser

from .serializers import (
    ResidentialPropertySerializer,
    BookVisitSerializer,
    CommercialPropertySerializer,
)
from .models import ResidentialProperty, BookVisit, CommercialProperty


class ResidentialPropertyView(APIView):
    serializer_class = ResidentialPropertySerializer
    permission_classes = [IsAuthenticated, IsLandlordUser]

    def get(self, request, id=None):

        properties = ResidentialProperty.objects.filter(user=request.user)
        serializer = ResidentialPropertySerializer(properties, many=True)
        return Response(serializer.data)

    def post(self, request, id=None):
        request.data["user"] = request.user.id
        serializer = ResidentialPropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        user = request.user
        try:
            property = ResidentialProperty.objects.get(pk=id, user=user)
        except ResidentialProperty.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ResidentialPropertySerializer(property, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, id, request):
        user = request.user
        try:
            property = ResidentialProperty.objects.get(pk=id, user=user)
        except ResidentialProperty.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        property.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommercialPropertyView(APIView):
    serializer_class = CommercialPropertySerializer
    permission_classes = [IsAuthenticated, IsLandlordUser]

    def get(self, request, id=None):

        properties = CommercialProperty.objects.filter(user=request.user)
        serializer = CommercialPropertySerializer(properties, many=True)
        return Response(serializer.data)

    def post(self, request, id=None):
        request.data["user"] = request.user.id
        serializer = CommercialPropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        user = request.user
        try:
            property = CommercialProperty.objects.get(pk=id, user=user)
        except CommercialProperty.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommercialPropertySerializer(property, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, id, request):
        user = request.user
        try:
            property = CommercialProperty.objects.get(pk=id, user=user)
        except CommercialProperty.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        property.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookVisitView(APIView):
    serializer_class = BookVisitSerializer

    def get(self, request, id=None):

        try:
            properties = BookVisit.objects.filter(user=request.user)
            serializer = BookVisitSerializer(properties, many=True)
            return Response(serializer.data)
        except BookVisit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
