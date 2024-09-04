from django.db import models
from user_auth.models import User
from cloudinary.models import CloudinaryField
# Create your models here.


ID_PROOF = (('passport', 'Passport'), ('driving_license', 'Driving License'),
            ('aadhar_card', 'Aadhar Card'), {'pan_card', 'Pan Card'}, {'voter_id', 'Voter ID'})


class TenantUserProfile(models.Model):
    gender = (('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))
    marital_status = (('Single', 'Single'), ('Married', 'Married'))
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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class IDProof(models.Model):
    id_proof = models.CharField(max_length=255)
    id_type = models.CharField(max_length=255, choices=ID_PROOF)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = CloudinaryField('image')
    created_at = models.DateTimeField(auto_now_add=True)
