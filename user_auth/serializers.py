from rest_framework import serializers
from .models import User
# from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, smart_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.exceptions import AuthenticationFailed
from .utils import send_transactional_email, Google, registerUser
from django.conf import settings


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=255, min_length=6, write_only=True)
    is_landlord = serializers.BooleanField(required=False)
    is_tenant = serializers.BooleanField(required=False)
    userType = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password2', 'is_landlord', 'is_tenant', 'userType']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password doesn't match")
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        
        user_type = attrs.get('userType')
        if user_type == 'tenant':
            attrs['is_landlord'] = False
            attrs['is_tenant'] = True
        elif user_type == 'landlord':
            attrs['is_landlord'] = True
            attrs['is_tenant'] = False
        else:
            raise serializers.ValidationError("Invalid user type")
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        validated_data.pop('userType')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    otp = serializers.CharField(max_length=6)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email does not exist")
            return attrs
        user = User.objects.get(email=email)
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        request = self.context['request']
        site_domain = get_current_site(request).domain

        relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
        abs_link = f"https://{site_domain}{relative_link}"
        email_body = f"Hello, \n Use the link below to reset your password \n {abs_link}"
        data = {'to_email': user.email,
                'email_subject': 'Reset your password',
                'email_body': email_body, }

        send_transactional_email(data)
        return attrs


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, write_only=True)
    confirmPassword = serializers.CharField(max_length=255, write_only=True)
    uidb64 = serializers.CharField(max_length=255, write_only=True)
    token = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        fields: ["password", "confirmPassword", "uidb64", "token"]  # noqa: F821

    def validate(self, attrs):
        try:
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            password = attrs.get('password')
            confirmPassword = attrs.get('confirmPassword')
            if password != confirmPassword:
                raise serializers.ValidationError("Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            user.set_password(password)
            user.save()
            return user
        except Exception as identifier:
            raise AuthenticationFailed(f"The reset link is invalid{identifier}", 401)


class GoogleSignInSerializer(serializers.Serializer):
    access_token = serializers.CharField()

    class Meta:
        fields = ['access_token']

    def validate_access_token(self, access_token):
        googleUserData = Google().validate(access_token)
        try:
            googleUserData['sub']
        except Exception as e:
            raise serializers.ValidationError(f"token expired or invalid {e}")

        if googleUserData['aud'] != settings.GOOGLE_OAUTH2_CLIENT_ID:
            raise AuthenticationFailed('Please continue your login using google')

        email = googleUserData['email']
        first_name = googleUserData['given_name']
        last_name = googleUserData.get('family_name', '')

        user_data = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'provider': 'google'
        }
        return registerUser(**user_data)
