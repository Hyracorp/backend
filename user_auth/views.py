
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from django.contrib.auth import authenticate
from rest_framework import status

from .serializers import UserRegisterSerializer, OTPVerificationSerializer, PasswordResetRequestSerializer, SetNewPasswordSerializer, GoogleSignInSerializer


from .utils import send_code_otp, verify_otp
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
# confirm password reset
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from .models import User
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class RegisterUserView(GenericAPIView):
    permission_classes = []
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user_data = serializer.data
            send_code_otp(user.email, user.first_name)
            return Response({
                'data': user_data,
                'message': 'User created successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendOTPView(GenericAPIView):
    permission_classes = []

    def post(self, request):
        data = request.data
        if 'email' not in data:
            return Response({
                'message': 'Email is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        email = data['email']
        try:
            user = User.objects.get(email=email)
            if user.is_verified:
                return Response({
                    'message': 'User already verified'
                }, status=status.HTTP_400_BAD_REQUEST)
            send_code_otp(email, user.first_name)
            return Response({
                'message': 'OTP sent successfully'
            }, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            raise ValueError("Email not found in database")


class VerifyUserView(GenericAPIView):
    permission_classes = []
    serializer_class = OTPVerificationSerializer

    def post(self, request):
        data = request.data
        email = data['email']
        otp = data['otp']

        try:
            user = User.objects.get(email=email)

        except ObjectDoesNotExist:
            raise ValueError("Email not found in database")

        if verify_otp(email, otp):
            user.is_verified = True
            user.is_active = True
            user.save()
            return Response({
                'message': 'OTP verified successfully'
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Invalid OTP'
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    permission_classes = []

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)

        if user is None:
            raise AuthenticationFailed('Invalid email or password')

        if not user.is_verified:
            raise AuthenticationFailed('Email not verified')

        tokens = user.tokens()

        # Determine the user type
        user_type = None
        if user.is_landlord:
            user_type = 'landlord'
        elif user.is_tenant:
            user_type = 'tenant'

        # Prepare the response
        res = Response({
            "message": "Login successful",
            "access_token": tokens.get('access'),
            "user_type": user_type  # Add user type to the response
        }, status=status.HTTP_200_OK)

        # Set the refresh token in a cookie
        res.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=tokens.get('refresh'),
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        return res


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Extract the refresh token from the cookie
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])

        if not refresh_token:
            return Response({"detail": "Refresh token cookie not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare data for the serializer
        data = {'refresh': refresh_token}

        # Use the default TokenRefreshSerializer to validate and generate a new access token
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Return the new access token
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class PasswordResetRequestView(APIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = []

    def post(self, request: Request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Password reset link sent to email"}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    permission_classes = []

    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            return Response({
                'message': 'Credentials Valid',
                'uidb64': uidb64,
                'token': token
            })
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed(
                    f"The reset link is invalid {identifier}", 401)


class SetNewPasswordView(APIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = []

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)


class GoogleSignInView(APIView):
    permission_classes = []
    serializer_class = GoogleSignInSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        uData = serializer.data
        print(uData.get('access_token'))
        return Response({'data': {'access': uData['access_token']}}, status=status.HTTP_200_OK)
