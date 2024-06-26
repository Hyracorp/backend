# Generated by Django 5.0.4 on 2024-06-03 01:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Amenity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("icon", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="BaseProperty",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "property_type",
                    models.CharField(
                        choices=[
                            ("Residential", "Residential"),
                            ("Commercial", "Commercial"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "service_type",
                    models.CharField(
                        choices=[
                            ("Lease", "Lease"),
                            ("Rent", "Rent"),
                            ("Management", "Management"),
                        ],
                        max_length=20,
                    ),
                ),
                ("area_sq_ft", models.FloatField()),
                ("floor_no", models.CharField(max_length=20)),
                ("expected_rate_rent", models.FloatField()),
                ("property_insured", models.BooleanField()),
                ("title", models.CharField(max_length=255)),
                ("property_location", models.CharField(max_length=255)),
                ("address_line1", models.CharField(max_length=255)),
                ("address_line2", models.CharField(blank=True, max_length=255)),
                ("pincode", models.CharField(max_length=10)),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=100)),
                ("approved", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "amenities",
                    models.ManyToManyField(
                        blank=True, to="property_management.amenity"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="properties",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CommercialProperty",
            fields=[
                (
                    "baseproperty_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="property_management.baseproperty",
                    ),
                ),
                ("tenant_preference", models.CharField(max_length=100)),
                ("fire_safety_status", models.BooleanField()),
                ("washroom_facility", models.BooleanField()),
                ("generator", models.BooleanField()),
                ("no_of_car_parkings", models.IntegerField()),
                ("no_of_bike_parkings", models.IntegerField()),
            ],
            bases=("property_management.baseproperty",),
        ),
        migrations.CreateModel(
            name="ResidentialProperty",
            fields=[
                (
                    "baseproperty_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="property_management.baseproperty",
                    ),
                ),
                (
                    "bhk",
                    models.CharField(
                        choices=[
                            ("1 BHK", "1 BHK"),
                            ("2 BHK", "2 BHK"),
                            ("3 BHK", "3 BHK"),
                            ("4 BHK", "4 BHK"),
                        ],
                        max_length=10,
                    ),
                ),
                ("flat_house", models.CharField(max_length=10)),
                ("pets_allowed", models.BooleanField()),
                ("furnished", models.BooleanField()),
                ("power_backup", models.BooleanField()),
                ("non_veg_allowed", models.BooleanField()),
                ("landmark", models.CharField(blank=True, max_length=255)),
            ],
            bases=("property_management.baseproperty",),
        ),
        migrations.CreateModel(
            name="PropertyPhoto",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("photo_url", models.URLField()),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="photos",
                        to="property_management.baseproperty",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BookVisit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("time", models.TimeField()),
                (
                    "visit_status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("No Show", "No Show"),
                            ("Approved", "Approved"),
                            ("Cancelled", "Cancelled"),
                            ("Rejected", "Rejected"),
                            ("Finalized", "Finalized"),
                        ],
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="property_management.residentialproperty",
                    ),
                ),
            ],
        ),
    ]
