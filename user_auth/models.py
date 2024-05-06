from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .manager import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.


AUTH_PROVIDERS={
    'email':'email',
    'google':'google',
    'facebook':'facebook'
}

class User(AbstractBaseUser,PermissionsMixin):
    id=models.BigAutoField(primary_key=True)
    email=models.EmailField(unique=True)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    is_verified=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    is_landlord = models.BooleanField(default=False)
    is_tenant = models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    auth_provider=models.CharField(max_length=255,blank=False,null=False,choices=AUTH_PROVIDERS.items(),default='email')
    
    USERNAME_FIELD='email'
    
    REQUIRED_FIELDS=['first_name','last_name']
    objects=UserManager()

    def __str__(self):
        return self.email
    
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
        


class OneTimePassword(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE),
    counter=models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user} passcode"
    