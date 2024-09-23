from .models import Notification

# Helper methods to create notifications


def create_user_notification(user, notification_type, message, action_link=None, content_object=None):
    return Notification.objects.create(
        recipient_type='user',
        recipient=user,
        notification_type=notification_type,
        message=message,
        action_link=action_link,
        content_object=content_object
    )

def create_group_notification(group, notification_type, message, action_link=None, content_object=None):
    return Notification.objects.create(
        recipient_type='group',
        recipient=group,
        notification_type=notification_type,
        message=message,
        action_link=action_link,
        content_object=content_object
    )
