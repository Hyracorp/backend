# Generated by Django 5.0.4 on 2024-09-05 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property_management', '0007_alter_baseproperty_floor_no_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='propertyphoto',
            name='alt_text',
        ),
    ]
