from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSerializer,OTPVerificationSerializer,PasswordResetRequestSerializer,SetNewPasswordSerializer,GoogleSignInSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from django.contrib.auth import authenticate
from rest_framework import status
from .utils import send_code_otp,verify_otp
from django.core.exceptions import ObjectDoesNotExist
from .models import User,OneTimePassword
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed



# confirm password reset
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings

class RegisterUserView(GenericAPIView):
    permission_classes = []
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
    permission_classes = []
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





class LoginUserView(APIView):
    permission_classes = []
    def post(self,request:Request):
      
        data=request.data
        res = Response()
        email=data.get('email')
        password=data.get('password')
        user=authenticate(email=email,password=password)
        
        if user is None:
            raise AuthenticationFailed('User not found')
            
        if user.is_verified is False:
            raise AuthenticationFailed('Email not verified')
        tokens=user.tokens()
        res.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=tokens.get('refresh'),
                    expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
        response={
            "message":"Login successful",
            "tokens":tokens.get('access'),
        }
        res.data=response
        res.status_code=status.HTTP_200_OK
        
        return res

        
    def get(self,request:Request):
        content={
            "user":str(request.user),
            "auth":str(request.auth),
        }
        return Response(data=content,status=status.HTTP_200_OK)


class PasswordResetRequestView(APIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = []
    def post(self,request:Request):
        serializer=self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response({"message":"Password reset link sent to email"},status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    permission_classes=[]
    def get(self,request,uidb64,token):
        try:
            user_id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise AuthenticationFailed('The reset link is invalid',401)
            return Response({
                'message':'Credentials Valid',
                'uidb64':uidb64,
                'token':token
            })
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise AuthenticationFailed('The reset link is invalid',401)


class SetNewPasswordView(APIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = []
    def patch(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message':'Password reset successful'},status=status.HTTP_200_OK)

class GoogleSignInView(APIView):
    permission_classes = []
    serializer_class = GoogleSignInSerializer
    def post(self,request):
        data = request.data
        serializer=self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        uData=serializer.data
        print(uData.get('access_token'))
        return Response({'data':{'access':uData['access_token']}},status=status.HTTP_200_OK)
        
