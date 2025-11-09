from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from .models import Book, Library, Author
from django.forms import ModelForm

class BookForm(ModelForm):
    """Form for Book model."""
    class Meta:
        model = Book
        fields = ['title', 'author']

def list_books(request):
    """Display a list of all books."""
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    """Display details for a specific library."""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

def register(request):
    """
    Handle user registration.
    GET: Display registration form
    POST: Process registration, create user, auto-login, redirect
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('relationship_app:list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


def is_admin(user):
    """Check if user has Admin role."""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Admin'


def is_librarian(user):
    """Check if user has Librarian role."""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Librarian'


def is_member(user):
    """Check if user has Member role."""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Member'


@user_passes_test(is_admin, login_url='relationship_app:login')
def admin_view(request):
    """Admin view accessible only to users with Admin role."""
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(is_librarian, login_url='relationship_app:login')
def librarian_view(request):
    """Librarian view accessible only to users with Librarian role."""
    return render(request, 'relationship_app/librarian_view.html')


@user_passes_test(is_member, login_url='relationship_app:login')
def member_view(request):
    """Member view accessible only to users with Member role."""
    return render(request, 'relationship_app/member_view.html')


@permission_required('relationship_app.can_add_book', login_url='relationship_app:login')
def add_book(request):
    """View to add a new book. Requires can_add_book permission."""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully.')
            return redirect('relationship_app:list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})


@permission_required('relationship_app.can_change_book', login_url='relationship_app:login')
def edit_book(request, pk):
    """View to edit an existing book. Requires can_change_book permission."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully.')
            return redirect('relationship_app:list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})


@permission_required('relationship_app.can_delete_book', login_url='relationship_app:login')
def delete_book(request, pk):
    """View to delete a book. Requires can_delete_book permission."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully.')
        return redirect('relationship_app:list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})