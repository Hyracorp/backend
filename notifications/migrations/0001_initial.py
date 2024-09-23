# Generated by Django 5.0.4 on 2024-09-23 13:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient_type', models.CharField(choices=[('user', 'User'), ('group', 'Group')], max_length=5)),
                ('recipient_id', models.PositiveIntegerField()),
                ('notification_type', models.CharField(choices=[('booking_approved', 'Booking Approved'), ('booking_rejected', 'Booking Rejected'), ('booking_cancelled', 'Booking Cancelled'), ('booking_rescheduled', 'Booking Rescheduled'), ('booking_confirmed', 'Booking Confirmed'), ('booking_request', 'Booking Request'), ('property_approved', 'Property Approved'), ('property_rejected', 'Property Rejected'), ('property_photo_approved', 'Property Photo Approved'), ('property_photo_rejected', 'Property Photo Rejected')], max_length=50)),
                ('message', models.TextField()),
                ('action_link', models.URLField(blank=True, null=True)),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='contenttypes.contenttype')),
                ('recipient_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'indexes': [models.Index(fields=['recipient_type', 'recipient_id'], name='notificatio_recipie_e8689e_idx'), models.Index(fields=['notification_type'], name='notificatio_notific_f2898f_idx'), models.Index(fields=['is_read'], name='notificatio_is_read_9edb86_idx')],
            },
        ),
    ]
