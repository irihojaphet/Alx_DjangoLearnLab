"""
Forms for the bookshelf application.

This module contains form definitions with proper validation and sanitization
to prevent security vulnerabilities such as SQL injection and XSS attacks.

SECURITY NOTES:
- Django forms automatically validate and sanitize user input
- All form fields are validated against model constraints
- Output is automatically escaped in templates to prevent XSS attacks
- Django ORM uses parameterized queries, preventing SQL injection
"""

from django import forms
from .models import Book


class ExampleForm(forms.ModelForm):
    """
    Example form for Book model demonstrating secure form handling.
    
    This form validates user input and prevents SQL injection and XSS attacks.
    
    SECURITY: Django ModelForm automatically:
    - Validates input data against model field definitions
    - Sanitizes user input to prevent SQL injection
    - Escapes HTML in templates (when using {{ form.field }})
    - Prevents XSS attacks through Django's template escaping
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        
        # Optional: Add widget customization for better security
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
        # Optional: Add labels
        labels = {
            'title': 'Book Title',
            'author': 'Author Name',
            'publication_year': 'Publication Year',
        }

