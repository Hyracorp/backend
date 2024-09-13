from django.db import models

# Create your models here.

class PublicData(models.Model):
    phone_1 = models.CharField(max_length=13)
    phone_2 = models.CharField(max_length=13)
    email = models.EmailField()
    website = models.URLField()
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

