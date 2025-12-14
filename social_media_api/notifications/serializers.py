from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model"""
    actor = serializers.StringRelatedField(read_only=True)
    recipient = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = (
            'id', 'recipient', 'actor', 'verb', 'target_content_type',
            'target_object_id', 'timestamp', 'read'
        )
        read_only_fields = ('id', 'recipient', 'actor', 'verb', 'target_content_type',
                          'target_object_id', 'timestamp')

