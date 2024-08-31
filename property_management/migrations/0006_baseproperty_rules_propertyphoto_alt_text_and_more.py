# Generated by Django 5.0.4 on 2024-08-31 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property_management', '0005_remove_baseproperty_property_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseproperty',
            name='rules',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='propertyphoto',
            name='alt_text',
            field=models.CharField(default='some-photo', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='propertyphoto',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='propertyphoto',
            name='title',
            field=models.CharField(default='property_photo', max_length=255),
            preserve_default=False,
        ),
    ]