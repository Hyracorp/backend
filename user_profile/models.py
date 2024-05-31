from django.db import models
from user_auth.models import User
# Create your models here.


class TenantUserProfile(models.Model):
    gender = (('male', 'Male'), ('female', 'Female'), ('other', 'Other'))
    marital_status = (('unmarried', 'Unmarried'), ('married', 'Married'))
    tId = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255, blank=False, null=False)
    gender = models.CharField(max_length=255, choices=gender)
    occupation = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    id_proof = models.CharField(blank=True)
    marital_status = models.CharField(max_length=255, choices=marital_status)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class LandlordUserProfile(models.Model):
    lId = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255, blank=False, null=False)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    id_proof = models.CharField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
