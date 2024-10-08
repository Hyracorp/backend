from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group
from .manager import UserManager
from django.contrib.auth.hashers import make_password
# Create your models here.


AUTH_PROVIDERS = {
    'email': 'email',
    'google': 'google',
    'facebook': 'facebook'
}


class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_landlord = models.BooleanField(default=False)
    is_tenant = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    auth_provider = models.CharField(
        max_length=255, blank=False, null=False, choices=AUTH_PROVIDERS.items(), default='email')

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Check if the password is already hashed
        if self.pk is None or 'pbkdf2_' not in self.password:
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def add_to_group(self, group_name):
        group = Group.objects.get(name=group_name)
        self.groups.add(group)


class OneTimePassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE),
    counter = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} passcode"
