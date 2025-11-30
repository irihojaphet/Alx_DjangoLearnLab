# Django REST Framework API Views Documentation

This document provides comprehensive documentation for the custom views implemented in the advanced-api-project using Django REST Framework's generic views and mixins.

## Table of Contents

1. [Overview](#overview)
2. [View Architecture](#view-architecture)
3. [API Endpoints](#api-endpoints)
4. [Permissions](#permissions)
5. [View Details](#view-details)
6. [Customization](#customization)
7. [Testing](#testing)
8. [Usage Examples](#usage-examples)

## Overview

The API implements a complete CRUD (Create, Read, Update, Delete) interface for the Book model using Django REST Framework's generic views. Each view is designed to handle specific operations efficiently while maintaining proper permissions and data validation.

### Key Features

- **Generic Views**: Utilizes DRF's generic views for streamlined development
- **Permission-Based Access**: Different permission levels for read and write operations
- **Custom Validation**: Integrated with custom serializers for data validation
- **Optimized Queries**: Uses `select_related` to reduce database queries
- **Custom Responses**: Enhanced response messages for better API usability

## View Architecture

The views are organized using Django REST Framework's generic view classes:

- `ListAPIView` - For listing multiple objects
- `RetrieveAPIView` - For retrieving a single object
- `CreateAPIView` - For creating new objects
- `UpdateAPIView` - For updating existing objects
- `DestroyAPIView` - For deleting objects

Each view extends the appropriate generic view class and customizes behavior as needed.

## API Endpoints

### Base URL
All API endpoints are prefixed with `/api/`

### Endpoint Summary

| Method | Endpoint | View | Permission | Description |
|--------|----------|------|------------|-------------|
| GET | `/api/books/` | BookListView | AllowAny | List all books |
| GET | `/api/books/<int:pk>/` | BookDetailView | AllowAny | Retrieve single book |
| POST | `/api/books/create/` | BookCreateView | IsAuthenticated | Create new book |
| PUT/PATCH | `/api/books/<int:pk>/update/` | BookUpdateView | IsAuthenticated | Update existing book |
| DELETE | `/api/books/<int:pk>/delete/` | BookDeleteView | IsAuthenticated | Delete book |

## Permissions

The API implements a two-tier permission system:

### Public Read Access (AllowAny)
- **ListView** (`/api/books/`): Anyone can view the list of books
- **DetailView** (`/api/books/<int:pk>/`): Anyone can view individual book details

### Authenticated Write Access (IsAuthenticated)
- **CreateView** (`/api/books/create/`): Only authenticated users can create books
- **UpdateView** (`/api/books/<int:pk>/update/`): Only authenticated users can update books
- **DeleteView** (`/api/books/<int:pk>/delete/`): Only authenticated users can delete books

### Permission Implementation

Permissions are set using DRF's permission classes:

```python
# Public access
permission_classes = [permissions.AllowAny]

# Authenticated only
permission_classes = [permissions.IsAuthenticated]
```

## View Details

### 1. BookListView

**Purpose**: Retrieve a list of all books in the database.

**Endpoint**: `GET /api/books/`

**Permissions**: `AllowAny` (public read access)

**Features**:
- Returns all books ordered by publication year (newest first), then by title
- Uses `select_related('author')` to optimize database queries
- Automatically handles pagination if configured

**Response Format**:
```json
[
    {
        "id": 1,
        "title": "1984",
        "publication_year": 1949,
        "author": 1
    },
    {
        "id": 2,
        "title": "Animal Farm",
        "publication_year": 1945,
        "author": 1
    }
]
```

### 2. BookDetailView

**Purpose**: Retrieve a single book by its primary key.

**Endpoint**: `GET /api/books/<int:pk>/`

**Permissions**: `AllowAny` (public read access)

**Features**:
- Returns detailed information about a specific book
- Uses `select_related('author')` to optimize database queries
- Automatically returns 404 if book doesn't exist

**Response Format**:
```json
{
    "id": 1,
    "title": "1984",
    "publication_year": 1949,
    "author": 1
}
```

**Error Response** (404):
```json
{
    "detail": "Not found."
}
```

### 3. BookCreateView

**Purpose**: Create a new book instance.

**Endpoint**: `POST /api/books/create/`

**Permissions**: `IsAuthenticated` (requires authentication)

**Features**:
- Validates incoming data using BookSerializer
- Custom validation ensures publication_year is not in the future
- Returns custom success message with created book data
- Automatically handles validation errors

**Request Body**:
```json
{
    "title": "The Great Gatsby",
    "publication_year": 1925,
    "author": 1
}
```

**Success Response** (201 Created):
```json
{
    "message": "Book created successfully",
    "data": {
        "id": 3,
        "title": "The Great Gatsby",
        "publication_year": 1925,
        "author": 1
    }
}
```

**Error Response** (400 Bad Request):
```json
{
    "publication_year": [
        "Publication year cannot be in the future. Current year is 2024."
    ]
}
```

**Error Response** (401 Unauthorized):
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 4. BookUpdateView

**Purpose**: Update an existing book instance.

**Endpoint**: 
- `PUT /api/books/<int:pk>/update/` (full update)
- `PATCH /api/books/<int:pk>/update/` (partial update)

**Permissions**: `IsAuthenticated` (requires authentication)

**Features**:
- Supports both PUT (full update) and PATCH (partial update)
- Validates incoming data using BookSerializer
- Custom validation ensures publication_year is not in the future
- Returns custom success message with updated book data

**Request Body** (PUT - full update):
```json
{
    "title": "1984 (Updated)",
    "publication_year": 1949,
    "author": 1
}
```

**Request Body** (PATCH - partial update):
```json
{
    "title": "1984 (Updated)"
}
```

**Success Response** (200 OK):
```json
{
    "message": "Book updated successfully",
    "data": {
        "id": 1,
        "title": "1984 (Updated)",
        "publication_year": 1949,
        "author": 1
    }
}
```

**Error Response** (404 Not Found):
```json
{
    "detail": "Not found."
}
```

### 5. BookDeleteView

**Purpose**: Delete a book instance from the database.

**Endpoint**: `DELETE /api/books/<int:pk>/delete/`

**Permissions**: `IsAuthenticated` (requires authentication)

**Features**:
- Permanently removes the book from the database
- Returns custom success message with book title
- Automatically handles cascade deletions (if configured)

**Success Response** (204 No Content):
```json
{
    "message": "Book \"1984\" deleted successfully"
}
```

**Error Response** (404 Not Found):
```json
{
    "detail": "Not found."
}
```

## Customization

### Custom Methods and Hooks

Each view includes custom methods that extend the default behavior:

#### perform_create (CreateView)
Called after validation but before saving. Can be used to:
- Set additional fields
- Perform side effects
- Add custom logic

#### perform_update (UpdateView)
Called after validation but before saving. Can be used to:
- Track changes
- Perform side effects
- Add custom logic

#### get_queryset
Customizes the queryset for optimization:
- Uses `select_related('author')` to reduce database queries
- Applies ordering (newest books first)

#### Custom Response Format
All write operations (create, update, delete) return custom response messages for better API usability.

### Adding Filters

To add filtering capabilities, you can extend the `get_queryset` method:

```python
def get_queryset(self):
    queryset = Book.objects.select_related('author')
    author_id = self.request.query_params.get('author', None)
    if author_id:
        queryset = queryset.filter(author_id=author_id)
    return queryset.order_by('-publication_year', 'title')
```

### Adding Search

To add search functionality, you can use DRF's SearchFilter:

```python
from rest_framework import filters

class BookListView(generics.ListAPIView):
    search_fields = ['title', 'author__name']
    filter_backends = [filters.SearchFilter]
    # ... rest of the view
```

## Testing

### Manual Testing with curl

#### 1. List All Books (Public)
```bash
curl -X GET http://localhost:8000/api/books/
```

#### 2. Retrieve Single Book (Public)
```bash
curl -X GET http://localhost:8000/api/books/1/
```

#### 3. Create Book (Requires Authentication)
```bash
curl -X POST http://localhost:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -d '{
    "title": "Test Book",
    "publication_year": 2023,
    "author": 1
  }'
```

#### 4. Update Book (Requires Authentication)
```bash
curl -X PUT http://localhost:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -d '{
    "title": "Updated Book Title",
    "publication_year": 2023,
    "author": 1
  }'
```

#### 5. Delete Book (Requires Authentication)
```bash
curl -X DELETE http://localhost:8000/api/books/1/delete/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Testing Permissions

#### Test Unauthenticated Access to Write Operations
```bash
# This should return 401 Unauthorized
curl -X POST http://localhost:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Book",
    "publication_year": 2023,
    "author": 1
  }'
```

#### Test Authenticated Access
1. Create a superuser: `python manage.py createsuperuser`
2. Obtain authentication token (if using token authentication)
3. Include token in request headers

### Testing with Django Shell

```python
from api.models import Author, Book
from api.serializers import BookSerializer
from rest_framework.test import APIClient

# Create test data
author = Author.objects.create(name="Test Author")
book = Book.objects.create(
    title="Test Book",
    publication_year=2023,
    author=author
)

# Test serializer
serializer = BookSerializer(book)
print(serializer.data)

# Test API client
client = APIClient()
response = client.get('/api/books/')
print(response.data)
```

## Usage Examples

### Python Requests Library

```python
import requests

BASE_URL = "http://localhost:8000/api"

# List all books (no authentication required)
response = requests.get(f"{BASE_URL}/books/")
books = response.json()
print(books)

# Get single book (no authentication required)
response = requests.get(f"{BASE_URL}/books/1/")
book = response.json()
print(book)

# Create book (authentication required)
headers = {
    "Authorization": "Token YOUR_TOKEN_HERE",
    "Content-Type": "application/json"
}
data = {
    "title": "New Book",
    "publication_year": 2023,
    "author": 1
}
response = requests.post(
    f"{BASE_URL}/books/create/",
    json=data,
    headers=headers
)
print(response.json())

# Update book (authentication required)
data = {
    "title": "Updated Book Title",
    "publication_year": 2023,
    "author": 1
}
response = requests.put(
    f"{BASE_URL}/books/1/update/",
    json=data,
    headers=headers
)
print(response.json())

# Delete book (authentication required)
response = requests.delete(
    f"{BASE_URL}/books/1/delete/",
    headers=headers
)
print(response.json())
```

### JavaScript Fetch API

```javascript
const BASE_URL = 'http://localhost:8000/api';

// List all books
fetch(`${BASE_URL}/books/`)
  .then(response => response.json())
  .then(data => console.log(data));

// Create book (with authentication)
fetch(`${BASE_URL}/books/create/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Token YOUR_TOKEN_HERE'
  },
  body: JSON.stringify({
    title: 'New Book',
    publication_year: 2023,
    author: 1
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## Configuration Files

### URL Configuration (`api/urls.py`)
All URL patterns are defined in `api/urls.py` with clear naming conventions and documentation.

### Main URL Configuration (`advanced_api_project/urls.py`)
API URLs are included in the main project's URL configuration:
```python
path('api/', include('api.urls')),
```

## Best Practices

1. **Always validate data**: The serializers handle validation automatically
2. **Use appropriate permissions**: Public read, authenticated write
3. **Optimize queries**: Use `select_related` for foreign key relationships
4. **Provide clear error messages**: Custom responses help API consumers
5. **Document endpoints**: Clear documentation improves API usability
6. **Test thoroughly**: Test both success and error cases
7. **Handle edge cases**: Consider 404s, validation errors, and permission errors

## Troubleshooting

### Common Issues

1. **401 Unauthorized**: Ensure you're including authentication credentials for write operations
2. **404 Not Found**: Verify the book ID exists in the database
3. **400 Bad Request**: Check that all required fields are provided and validation passes
4. **500 Internal Server Error**: Check server logs for detailed error information

### Debugging Tips

- Use Django's debug toolbar in development
- Check `python manage.py check` for configuration issues
- Review serializer validation errors in API responses
- Test endpoints individually to isolate issues

## Future Enhancements

Potential improvements to consider:

1. **Pagination**: Implement pagination for list views
2. **Filtering**: Add filtering by author, publication year, etc.
3. **Search**: Implement full-text search on book titles
4. **Rate Limiting**: Add rate limiting to prevent abuse
5. **Caching**: Implement caching for frequently accessed data
6. **Versioning**: Add API versioning for future changes
7. **Documentation**: Generate OpenAPI/Swagger documentation

---

**Last Updated**: 2024
**Project**: advanced-api-project
**Framework**: Django REST Framework

