"""
Views for Book management with permission-based access control.

This module implements CRUD operations for the Book model, with each view
protected by specific permissions:

- list_books and book_detail: Require 'bookshelf.can_view' permission
- create_book: Requires 'bookshelf.can_create' permission
- edit_book: Requires 'bookshelf.can_edit' permission
- delete_book: Requires 'bookshelf.can_delete' permission

Users must be assigned to groups (Viewers, Editors, Admins) or have
individual permissions assigned to access these views.

For more information on permissions and groups, see PERMISSIONS_AND_GROUPS.md
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from django.forms import ModelForm
from .models import Book


class BookForm(ModelForm):
    """Form for Book model."""
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def list_books(request):
    """Display a list of all books. Requires can_view permission."""
    books = Book.objects.all()
    return render(request, 'bookshelf/list_books.html', {'books': books})


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
    """Display details for a specific book. Requires can_view permission."""
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})


@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    """View to create a new book. Requires can_create permission."""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book created successfully.')
            return redirect('bookshelf:list_books')
    else:
        form = BookForm()
    return render(request, 'bookshelf/create_book.html', {'form': form})


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    """View to edit an existing book. Requires can_edit permission."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully.')
            return redirect('bookshelf:list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/edit_book.html', {'form': form, 'book': book})


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    """View to delete a book. Requires can_delete permission."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully.')
        return redirect('bookshelf:list_books')
    return render(request, 'bookshelf/delete_book.html', {'book': book})
