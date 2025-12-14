from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class Notification(models.Model):
    """Notification model for user notifications"""
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text="User who receives the notification"
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='actions',
        help_text="User who performed the action"
    )
    verb = models.CharField(
        max_length=255,
        help_text="Action description (e.g., 'liked your post', 'commented on your post', 'started following you')"
    )
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Content type of the target object"
    )
    target_object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="ID of the target object"
    )
    target = GenericForeignKey('target_content_type', 'target_object_id')
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the notification was created"
    )
    read = models.BooleanField(
        default=False,
        help_text="Whether the notification has been read"
    )

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return f"{self.actor.username} {self.verb} - {self.recipient.username}"
