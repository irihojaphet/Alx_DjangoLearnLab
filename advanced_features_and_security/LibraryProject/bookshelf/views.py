"""
Views for Book management with permission-based access control.

This module implements CRUD operations for the Book model, with each view
protected by specific permissions:

- book_list and book_detail: Require 'bookshelf.can_view' permission
- create_book: Requires 'bookshelf.can_create' permission
- edit_book: Requires 'bookshelf.can_edit' permission
- delete_book: Requires 'bookshelf.can_delete' permission

Users must be assigned to groups (Viewers, Editors, Admins) or have
individual permissions assigned to access these views.

SECURITY NOTES:
- All views use Django ORM (e.g., Book.objects.all(), get_object_or_404)
  which prevents SQL injection by using parameterized queries automatically
- All user input is validated through Django ModelForm which sanitizes
  and validates data before saving to database
- CSRF protection is enforced via @csrf_protect (automatic with forms using {% csrf_token %})
- All views require authentication (@login_required) and specific permissions
- get_object_or_404() prevents direct object access without proper handling
- Form validation prevents XSS by escaping output automatically in templates

For more information on permissions and groups, see PERMISSIONS_AND_GROUPS.md
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from django.utils.html import escape
from .models import Book
from .forms import ExampleForm


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Display a list of all books. Requires can_view permission.
    
    SECURITY:
    - Uses Django ORM (Book.objects.all()) which prevents SQL injection
    - All output is escaped in templates using {{ variable|escape }}
    - Protected by login_required and permission_required decorators
    """
    # SECURITY: Django ORM automatically uses parameterized queries
    # No string formatting or raw SQL, preventing SQL injection
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
    """
    Display details for a specific book. Requires can_view permission.
    
    SECURITY:
    - get_object_or_404() safely handles the pk parameter, preventing SQL injection
    - pk is automatically validated and converted to integer by Django URL routing
    - Returns 404 for invalid/inaccessible objects instead of exposing errors
    - Output is escaped in templates using {{ variable|escape }}
    """
    # SECURITY: get_object_or_404 uses parameterized query, preventing SQL injection
    # The pk parameter is validated by Django URL routing before reaching this view
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})


@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    """
    View to create a new book. Requires can_create permission.
    
    SECURITY:
    - CSRF protection is enforced via CSRF middleware (automatic with {% csrf_token %})
    - BookForm.validate() ensures all input is validated and sanitized
    - form.save() uses Django ORM parameterized queries, preventing SQL injection
    - All user input is validated against model field constraints
    - Only allows POST requests for form submission (prevents CSRF via GET)
    """
    if request.method == 'POST':
        # SECURITY: Django ModelForm automatically validates and sanitizes input
        # CSRF token is validated by CsrfViewMiddleware before this view runs
        form = ExampleForm(request.POST)
        if form.is_valid():
            # SECURITY: form.save() uses Django ORM with parameterized queries
            # All field values are validated and escaped
            form.save()
            messages.success(request, 'Book created successfully.')
            return redirect('bookshelf:book_list')
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/create_book.html', {'form': form})


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    """
    View to edit an existing book. Requires can_edit permission.
    
    SECURITY:
    - get_object_or_404() prevents SQL injection and unauthorized object access
    - CSRF protection enforced via CSRF middleware
    - BookForm validates and sanitizes all user input before saving
    - form.save() uses parameterized queries, preventing SQL injection
    - pk is validated by Django URL routing before reaching this view
    """
    # SECURITY: Safe object retrieval using parameterized query
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        # SECURITY: Form instance ensures we're updating the correct object
        # All input is validated and sanitized by Django ModelForm
        form = ExampleForm(request.POST, instance=book)
        if form.is_valid():
            # SECURITY: ORM automatically handles SQL escaping
            form.save()
            messages.success(request, 'Book updated successfully.')
            return redirect('bookshelf:book_list')
    else:
        form = ExampleForm(instance=book)
    return render(request, 'bookshelf/edit_book.html', {'form': form, 'book': book})


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    """
    View to delete a book. Requires can_delete permission.
    
    SECURITY:
    - Requires POST method to prevent CSRF attacks via GET requests
    - get_object_or_404() safely retrieves object using parameterized query
    - CSRF token validation enforced by CSRF middleware
    - Double confirmation via template form prevents accidental deletions
    - pk is validated by Django URL routing before reaching this view
    """
    # SECURITY: Safe object retrieval prevents SQL injection
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        # SECURITY: POST-only deletion prevents CSRF via GET requests
        # Django ORM delete() uses parameterized queries
        book.delete()
        messages.success(request, 'Book deleted successfully.')
        return redirect('bookshelf:book_list')
    # GET request shows confirmation form (protected by CSRF token)
    return render(request, 'bookshelf/delete_book.html', {'book': book})
