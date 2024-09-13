from django.db import models
from user_auth.models import User
from cloudinary.models import CloudinaryField


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
    floor_no = models.CharField(max_length=100)
    expected_rate_rent = models.FloatField()
    expected_deposit = models.FloatField()
    description = models.TextField()
    property_owner = models.CharField(max_length=255)
    property_insured = models.BooleanField()
    title = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    pincode = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    amenities = models.ManyToManyField(Amenity, blank=True)
    rules = models.TextField(blank=True)

    def __str__(self):
        return self.title


class ResidentialProperty(BaseProperty):
    BHK_CHOICES = [
        (1, "1 BHK"),
        (2, "2 BHK"),
        (3, "3 BHK"),
        (4, "4 BHK"),
    ]

    bhk = models.IntegerField(choices=BHK_CHOICES)
    flat_house = models.CharField(max_length=100)
    pets_allowed = models.BooleanField()
    furnished = models.BooleanField()
    power_backup = models.BooleanField()
    non_veg_allowed = models.BooleanField()
    landmark = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.pk} {self.city} {self.title}"


class CommercialProperty(BaseProperty):

    tenant_preference = models.CharField(max_length=100)
    fire_safety_status = models.BooleanField()
    washroom_facility = models.BooleanField()
    generator = models.BooleanField()
    no_of_car_parkings = models.IntegerField()
    no_of_bike_parkings = models.IntegerField()

    def __str__(self):
        return f"{self.pk} {self.city}  {self.title}"


class PropertyPhoto(models.Model):
    property = models.ForeignKey(
        BaseProperty, on_delete=models.CASCADE, related_name="photos"
    )
    photo_url = CloudinaryField("image")
    title = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.property.title} {self.property.id}"


class BookVisit(models.Model):
    visit_status_choices = [
        ("Pending", "Pending"),
        ("No Show", "No Show"),
        ("Approved", "Approved"),
        ("Cancelled", "Cancelled"),
        ("Rejected", "Rejected"),
        ("Visited", "Visited"),
        ("Finalized", "Finalized"),
        ("Expired", "Expired"),
        ("Rescheduled", "Rescheduled"),
    ]
    gender_choices = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]
    # Define valid time slots
    time_choices = [
        ("09:00", "09:00 AM"),
        ("11:00", "11:00 AM"),
        ("13:00", "01:00 PM"),
        ("15:00", "03:00 PM"),
        ("17:00", "05:00 PM"),
        ("19:00", "07:00 PM"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(ResidentialProperty, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=gender_choices)
    phone = models.CharField(max_length=13)
    date = models.DateField()
    time = models.CharField(max_length=5, choices=time_choices)
    visit_status = models.CharField(max_length=20, choices=visit_status_choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property', 'date', 'time')
    def __str__(self):
        return f"{self.user.email} ( {self.visit_status} )"

class Agreement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(ResidentialProperty, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    agreement = CloudinaryField("image")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} {self.property.title}"

