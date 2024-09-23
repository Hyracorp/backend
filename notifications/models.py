
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Notification(models.Model):
    RECIPIENT_CHOICES = (
        ('user', 'User'),
        ('group', 'Group'),
    )

    NOTIFICATION_TYPES = (
        ('booking_approved', 'Booking Approved'),
        ('booking_rejected', 'Booking Rejected'),
        ('booking_cancelled', 'Booking Cancelled'),
        ('booking_rescheduled', 'Booking Rescheduled'),
        ('booking_confirmed', 'Booking Confirmed'),
        ('booking_request', 'Booking Request'),
        ('property_approved', 'Property Approved'),
        ('property_rejected', 'Property Rejected'),
        ('property_photo_approved', 'Property Photo Approved'),
        ('property_photo_rejected', 'Property Photo Rejected'),

        # Add more types as needed
    )

    recipient_type = models.CharField(max_length=5, choices=RECIPIENT_CHOICES)
    recipient_id = models.PositiveIntegerField()
    recipient_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE)
    recipient = GenericForeignKey('recipient_content_type', 'recipient_id')

    notification_type = models.CharField(
        max_length=50, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    action_link = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Optional: Link to the object that triggered the notification
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        indexes = [
            models.Index(fields=['recipient_type', 'recipient_id']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['is_read']),
        ]

    def __str__(self):
        return f"{self.get_notification_type_display()} for {self.recipient}: {self.message[:50]}..."
# Create your models here.
