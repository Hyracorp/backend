from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import TenantUserProfile, LandlordUserProfile
from .serializers import TenantUserProfileSerializer, LandlordUserProfileSerializer
from .permissions import IsTenantUser, IsLandlordUser


class TenantUserProfileView(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]

    def get(self, request):
        user = request.user
        tenant_profile = TenantUserProfile.objects.filter(user=user).first()
        user_data = {"id": user.id, "email": user.email,
                     "first_name": user.first_name, "last_name": user.last_name}
        if tenant_profile:
            serializer = TenantUserProfileSerializer(tenant_profile)
            data = serializer.data
            data["user_data"] = user_data
            return Response({"data": data}, status=status.HTTP_200_OK)
        else:
            return Response(
                data={"message": "Profile not found, pls update",
                      user: user_data},
                status=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request):
        request.data["user"] = request.user.id
        serializer = TenantUserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        if id is None:
            return Response(
                data={"message": "Id is required to update"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.data["user"] = request.user.id
        instance = TenantUserProfile.objects.get(pk=id)
        if request.user.id != instance.user.id:
            return Response(
                data={"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = TenantUserProfileSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LandlordUserProfileView(APIView):
    permission_classes = [IsAuthenticated, IsLandlordUser]

    def get(self, request):
        user = request.user
        landlord_profile = LandlordUserProfile.objects.filter(
            user=user).first()
        user_data = {"id": user.id, "email": user.email,
                     "first_name": user.first_name, "last_name": user.last_name}
        if landlord_profile:
            serializer = LandlordUserProfileSerializer(landlord_profile)
            data = serializer.data
            data["user_data"] = user_data
            return Response({"data": data}, status=status.HTTP_200_OK)
        else:
            return Response(
                data={"message": "Profile not found, pls update",
                      user: user_data},
                status=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request):
        request.data["user"] = request.user.id
        serializer = LandlordUserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        if id is None:
            return Response(
                data={"message": "Id is required to update"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.data["user"] = request.user.id
        instance = LandlordUserProfile.objects.get(pk=id)
        if request.user.id != instance.user.id:
            return Response(
                data={"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = LandlordUserProfileSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IDProofView(APIView):
    permission_classes = [IsAuthenticated, IsLandlordUser]

    def post(self, request):
        request.data["user"] = request.user.id
        serializer = TenantUserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
