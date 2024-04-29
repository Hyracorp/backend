from rest_framework import serializers
from .models import User

class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255,min_length=6,write_only=True)
    password2 = serializers.CharField(max_length=255,min_length=6,write_only=True)
    
    class Meta:
        model = User
        fields = ['email','first_name','last_name','password','password2']
    
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password doesn't match")
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        return attrs
    def create(self, validated_data):
        user=User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user

class OTPVerificationSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    otp = serializers.CharField(max_length=6)  
    