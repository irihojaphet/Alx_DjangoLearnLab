from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin configuration for Notification model"""
    list_display = ('recipient', 'actor', 'verb', 'read', 'timestamp')
    list_filter = ('read', 'timestamp', 'verb')
    search_fields = ('recipient__username', 'actor__username', 'verb')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
