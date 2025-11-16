"""
Models for the bookshelf application.

This module contains:
- CustomUser: Custom user model extending AbstractUser with date_of_birth and profile_photo fields
- CustomUserManager: Custom manager for user creation with support for additional fields
- Book: Book model with custom permissions (can_view, can_create, can_edit, can_delete)

The Book model defines custom permissions that are used to control access
to various operations. These permissions are assigned to groups:
- Viewers: can_view only
- Editors: can_view, can_create, can_edit
- Admins: can_view, can_create, can_edit, can_delete

For more information on permissions and groups, see PERMISSIONS_AND_GROUPS.md
"""

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    """Custom user manager for CustomUser model."""
    
    def create_user(self, username, email=None, password=None, date_of_birth=None, profile_photo=None, **extra_fields):
        """Create and return a regular user with the given credentials."""
        if not username:
            raise ValueError('The Username field must be set')
        
        email = self.normalize_email(email) if email else None
        user = self.model(
            username=username,
            email=email,
            date_of_birth=date_of_birth,
            profile_photo=profile_photo,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, date_of_birth=None, profile_photo=None, **extra_fields):
        """Create and return a superuser with the given credentials."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, date_of_birth, profile_photo, **extra_fields)


class CustomUser(AbstractUser):
    """Custom user model extending AbstractUser with additional fields."""
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Book(models.Model):
    """Book model with custom permissions for access control."""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
    
    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        permissions = [
            ('can_view', 'Can view book'),
            ('can_create', 'Can create book'),
            ('can_edit', 'Can edit book'),
            ('can_delete', 'Can delete book'),
        ]
