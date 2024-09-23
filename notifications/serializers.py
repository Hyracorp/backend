from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    recipient_display = serializers.SerializerMethodField()
    notification_type_display = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient_type', 'recipient_display', 'message', 'action_link',
            'is_read', 'created_at', 'notification_type', 'notification_type_display',
            'content_type', 'object_id',
        ]
        read_only_fields = [
            'id', 'recipient_display', 'notification_type_display', 'created_at',
        ]

    def get_recipient_display(self, obj):
        if obj.recipient_type == 'user':
            return str(obj.recipient)
        else:
            return obj.recipient.name

    def get_notification_type_display(self, obj):
        return dict(Notification.NOTIFICATION_TYPES).get(obj.notification_type)
