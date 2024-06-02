from django.contrib import admin
from .models import Amenity, ResidentialProperty, CommercialProperty, PropertyPhoto

admin.site.register(Amenity)
admin.site.register(ResidentialProperty)
admin.site.register(CommercialProperty)
admin.site.register(PropertyPhoto)
