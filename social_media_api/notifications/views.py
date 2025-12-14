from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing notifications.
    Users can only view their own notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return only notifications for the current user"""
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_read(self, request, pk=None):
        """Mark a notification as read"""
        notification = self.get_object()
        if notification.recipient != request.user:
            return Response(
                {'error': 'You can only mark your own notifications as read.'},
                status=status.HTTP_403_FORBIDDEN
            )
        notification.read = True
        notification.save()
        return Response(
            {'message': 'Notification marked as read.'},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        Notification.objects.filter(recipient=request.user, read=False).update(read=True)
        return Response(
            {'message': 'All notifications marked as read.'},
            status=status.HTTP_200_OK
        )
