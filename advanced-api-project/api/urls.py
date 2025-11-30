"""
URL configuration for the API app.

This module defines all URL patterns for the Book API endpoints.
Each view is mapped to a specific URL path that corresponds to its function.

URL Patterns:
    - /api/books/              -> BookListView (GET: list all books)
    - /api/books/<int:pk>/     -> BookDetailView (GET: retrieve single book)
    - /api/books/create/        -> BookCreateView (POST: create new book)
    - /api/books/<int:pk>/update/ -> BookUpdateView (PUT/PATCH: update book)
    - /api/books/<int:pk>/delete/ -> BookDeleteView (DELETE: delete book)
"""
from django.urls import path
from . import views

app_name = 'api'  # Namespace for the API app

urlpatterns = [
    # ListView: Retrieve all books
    # Endpoint: GET /api/books/
    # Permissions: AllowAny (public read access)
    path('books/', views.BookListView.as_view(), name='book-list'),
    
    # DetailView: Retrieve a single book by ID
    # Endpoint: GET /api/books/<int:pk>/
    # Permissions: AllowAny (public read access)
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    
    # CreateView: Add a new book
    # Endpoint: POST /api/books/create/
    # Permissions: IsAuthenticated (requires authentication)
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    
    # UpdateView: Modify an existing book
    # Endpoint: PUT/PATCH /api/books/<int:pk>/update/
    # Permissions: IsAuthenticated (requires authentication)
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    
    # DeleteView: Remove a book
    # Endpoint: DELETE /api/books/<int:pk>/delete/
    # Permissions: IsAuthenticated (requires authentication)
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
]

