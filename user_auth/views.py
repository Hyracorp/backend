from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSerializer,OTPVerificationSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import send_code_otp,verify_otp
from django.core.exceptions import ObjectDoesNotExist
from .models import User,OneTimePassword
class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer
    def post(self,request):
        data = request.data
       
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user=serializer.data
            send_code_otp(user['email'])
            return Response({
                'data':user,
                'message':'User created successfully'
                },status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyUserView(GenericAPIView):
    serializer_class=OTPVerificationSerializer
    def post(self,request):
        data = request.data
        email = data['email']
        otp = data['otp']
       
        try:
            user = User.objects.get(email=email)
           
        except ObjectDoesNotExist:
            raise ValueError("Email not found in database")
        
        if verify_otp(email,otp):
            user.is_verified = True
            user.is_active = True
            user.save()
            return Response({
                'message':'OTP verified successfully'
                },status=status.HTTP_200_OK)
        return Response({
            'message':'Invalid OTP'
            },status=status.HTTP_400_BAD_REQUEST)