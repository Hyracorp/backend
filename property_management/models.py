from django.db import models
from user_auth.models import User


class Amenity(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BaseProperty(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ("Residential", "Residential"),
        ("Commercial", "Commercial"),
    ]

    SERVICE_TYPE_CHOICES = [
        ("Lease", "Lease"),
        ("Rent", "Rent"),
        ("Management", "Management"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="properties")
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES)
    area_sq_ft = models.FloatField()
    floor_no = models.CharField(max_length=20)
    expected_rate_rent = models.FloatField()
    property_insured = models.BooleanField()
    title = models.CharField(max_length=255)
    property_location = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    pincode = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    amenities = models.ManyToManyField(Amenity, blank=True)

    def __str__(self):
        return self.title


class ResidentialProperty(BaseProperty):
    BHK_CHOICES = [
        ("1 BHK", "1 BHK"),
        ("2 BHK", "2 BHK"),
        ("3 BHK", "3 BHK"),
        ("4 BHK", "4 BHK"),
    ]

    bhk = models.CharField(max_length=10, choices=BHK_CHOICES)
    flat_house = models.CharField(max_length=10)
    pets_allowed = models.BooleanField()
    furnished = models.BooleanField()
    power_backup = models.BooleanField()
    non_veg_allowed = models.BooleanField()
    landmark = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title


class CommercialProperty(BaseProperty):

    tenant_preference = models.CharField(max_length=100)
    fire_safety_status = models.BooleanField()
    washroom_facility = models.BooleanField()
    generator = models.BooleanField()
    no_of_car_parkings = models.IntegerField()
    no_of_bike_parkings = models.IntegerField()

    def __str__(self):
        return self.title


class PropertyPhoto(models.Model):
    property = models.ForeignKey(
        BaseProperty, on_delete=models.CASCADE, related_name="photos"
    )
    photo_url = models.URLField()


class BookVisit(models.Model):
    visit_status_choices = [
        ("Pending", "Pending"),
        ("No Show", "No Show"),
        ("Approved", "Approved"),
        ("Cancelled", "Cancelled"),
        ("Rejected", "Rejected"),
        ("Finalized", "Finalized"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(ResidentialProperty, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    visit_status = models.CharField(max_length=20, choices=visit_status_choices)
    created_at = models.DateTimeField(auto_now_add=True)
