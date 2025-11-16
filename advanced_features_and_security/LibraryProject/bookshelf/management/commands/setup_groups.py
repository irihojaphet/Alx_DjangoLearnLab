"""
Management command to set up user groups with permissions.

This command creates three groups: Viewers, Editors, and Admins,
and assigns appropriate permissions to each group.

Groups and their permissions:
- Viewers: can_view permission (read-only access)
- Editors: can_view, can_create, can_edit permissions (can read, create, and edit)
- Admins: can_view, can_create, can_edit, can_delete permissions (full access)

Usage:
    python manage.py setup_groups
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book


class Command(BaseCommand):
    help = 'Creates groups (Viewers, Editors, Admins) and assigns permissions'

    def handle(self, *args, **options):
        # Get content type for Book model
        content_type = ContentType.objects.get_for_model(Book)
        
        # Get all Book permissions
        can_view = Permission.objects.get(
            codename='can_view',
            content_type=content_type
        )
        can_create = Permission.objects.get(
            codename='can_create',
            content_type=content_type
        )
        can_edit = Permission.objects.get(
            codename='can_edit',
            content_type=content_type
        )
        can_delete = Permission.objects.get(
            codename='can_delete',
            content_type=content_type
        )
        
        # Create Viewers group (read-only)
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        if created:
            viewers_group.permissions.add(can_view)
            self.stdout.write(self.style.SUCCESS('Created Viewers group with can_view permission'))
        else:
            # Add permission if group exists but doesn't have it
            if can_view not in viewers_group.permissions.all():
                viewers_group.permissions.add(can_view)
                self.stdout.write(self.style.SUCCESS('Updated Viewers group with can_view permission'))
            else:
                self.stdout.write(self.style.WARNING('Viewers group already exists with can_view permission'))
        
        # Create Editors group (read, create, edit)
        editors_group, created = Group.objects.get_or_create(name='Editors')
        editors_permissions = [can_view, can_create, can_edit]
        for perm in editors_permissions:
            if perm not in editors_group.permissions.all():
                editors_group.permissions.add(perm)
        if created:
            self.stdout.write(self.style.SUCCESS('Created Editors group with can_view, can_create, can_edit permissions'))
        else:
            self.stdout.write(self.style.SUCCESS('Updated Editors group with can_view, can_create, can_edit permissions'))
        
        # Create Admins group (full access)
        admins_group, created = Group.objects.get_or_create(name='Admins')
        admins_permissions = [can_view, can_create, can_edit, can_delete]
        for perm in admins_permissions:
            if perm not in admins_group.permissions.all():
                admins_group.permissions.add(perm)
        if created:
            self.stdout.write(self.style.SUCCESS('Created Admins group with can_view, can_create, can_edit, can_delete permissions'))
        else:
            self.stdout.write(self.style.SUCCESS('Updated Admins group with can_view, can_create, can_edit, can_delete permissions'))
        
        self.stdout.write(self.style.SUCCESS('\nSuccessfully set up all groups and permissions!'))

