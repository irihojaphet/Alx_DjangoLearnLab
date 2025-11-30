# API Filtering, Searching, and Ordering Documentation

This document provides comprehensive documentation for the filtering, searching, and ordering capabilities implemented in the Book API.

## Table of Contents

1. [Overview](#overview)
2. [Filtering](#filtering)
3. [Searching](#searching)
4. [Ordering](#ordering)
5. [Combining Features](#combining-features)
6. [Usage Examples](#usage-examples)
7. [Implementation Details](#implementation-details)

## Overview

The Book API now supports three powerful query capabilities:

- **Filtering**: Filter books by exact matches on specific fields
- **Searching**: Perform text searches across multiple fields
- **Ordering**: Sort results by any field in ascending or descending order

These features are implemented using Django REST Framework's built-in filter backends:
- `DjangoFilterBackend` for filtering
- `SearchFilter` for searching
- `OrderingFilter` for ordering

## Filtering

Filtering allows you to retrieve books that match specific criteria exactly.

### Available Filter Fields

- `title`: Filter by exact book title
- `author`: Filter by author ID
- `publication_year`: Filter by publication year

### Filter Syntax

Add query parameters to the URL:
```
GET /api/books/?field_name=value
```

### Filter Examples

#### Filter by Title
```bash
# Get books with exact title "1984"
GET /api/books/?title=1984
```

#### Filter by Author
```bash
# Get all books by author with ID 1
GET /api/books/?author=1
```

#### Filter by Publication Year
```bash
# Get all books published in 1949
GET /api/books/?publication_year=1949
```

#### Multiple Filters
```bash
# Combine multiple filters
GET /api/books/?author=1&publication_year=1949
```

### Filter Response Example

```json
[
    {
        "id": 1,
        "title": "1984",
        "publication_year": 1949,
        "author": 1
    }
]
```

## Searching

Searching allows you to perform text searches across multiple fields simultaneously.

### Searchable Fields

- `title`: Search in book titles
- `author__name`: Search in author names (using related field lookup)

### Search Syntax

Use the `search` query parameter:
```
GET /api/books/?search=search_term
```

The search is case-insensitive and performs partial matching.

### Search Examples

#### Search by Title
```bash
# Search for books with "orwell" in the title
GET /api/books/?search=orwell
```

#### Search by Author Name
```bash
# Search for books by authors with "rowling" in their name
GET /api/books/?search=rowling
```

#### General Search
```bash
# Search across all searchable fields
GET /api/books/?search=1984
```

### Search Response Example

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

## Ordering

Ordering allows you to sort the results by any field in ascending or descending order.

### Orderable Fields

- `title`: Order by book title
- `publication_year`: Order by publication year
- `id`: Order by book ID

### Ordering Syntax

Use the `ordering` query parameter:
```
GET /api/books/?ordering=field_name
```

For descending order, prefix the field name with a minus sign (`-`):
```
GET /api/books/?ordering=-field_name
```

### Default Ordering

If no ordering is specified, results are ordered by:
1. Publication year (newest first) - descending
2. Title (alphabetically) - ascending

### Ordering Examples

#### Order by Title (Ascending)
```bash
# Sort books alphabetically by title
GET /api/books/?ordering=title
```

#### Order by Title (Descending)
```bash
# Sort books in reverse alphabetical order
GET /api/books/?ordering=-title
```

#### Order by Publication Year (Ascending)
```bash
# Sort books by publication year (oldest first)
GET /api/books/?ordering=publication_year
```

#### Order by Publication Year (Descending)
```bash
# Sort books by publication year (newest first)
GET /api/books/?ordering=-publication_year
```

#### Multiple Field Ordering
```bash
# Order by publication year first, then by title
GET /api/books/?ordering=-publication_year,title
```

### Ordering Response Example

```json
[
    {
        "id": 3,
        "title": "The Great Gatsby",
        "publication_year": 1925,
        "author": 2
    },
    {
        "id": 1,
        "title": "1984",
        "publication_year": 1949,
        "author": 1
    }
]
```

## Combining Features

You can combine filtering, searching, and ordering in a single request.

### Combined Query Examples

#### Filter + Order
```bash
# Get books by author 1, ordered by publication year (newest first)
GET /api/books/?author=1&ordering=-publication_year
```

#### Search + Order
```bash
# Search for "orwell" and order by title
GET /api/books/?search=orwell&ordering=title
```

#### Filter + Search + Order
```bash
# Filter by year, search for "farm", and order by title
GET /api/books/?publication_year=1945&search=farm&ordering=title
```

### Combined Query Response Example

```json
[
    {
        "id": 2,
        "title": "Animal Farm",
        "publication_year": 1945,
        "author": 1
    }
]
```

## Usage Examples

### Using curl

#### Basic List
```bash
curl -X GET http://localhost:8000/api/books/
```

#### Filter by Author
```bash
curl -X GET "http://localhost:8000/api/books/?author=1"
```

#### Search
```bash
curl -X GET "http://localhost:8000/api/books/?search=orwell"
```

#### Order by Title
```bash
curl -X GET "http://localhost:8000/api/books/?ordering=title"
```

#### Combined Query
```bash
curl -X GET "http://localhost:8000/api/books/?author=1&ordering=-publication_year&search=1984"
```

### Using Python requests

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Basic list
response = requests.get(f"{BASE_URL}/books/")
books = response.json()

# Filter by author
response = requests.get(f"{BASE_URL}/books/", params={"author": 1})
books = response.json()

# Search
response = requests.get(f"{BASE_URL}/books/", params={"search": "orwell"})
books = response.json()

# Order by publication year
response = requests.get(f"{BASE_URL}/books/", params={"ordering": "-publication_year"})
books = response.json()

# Combined: Filter + Search + Order
response = requests.get(
    f"{BASE_URL}/books/",
    params={
        "author": 1,
        "search": "orwell",
        "ordering": "-publication_year"
    }
)
books = response.json()
```

### Using JavaScript fetch

```javascript
const BASE_URL = 'http://localhost:8000/api';

// Basic list
fetch(`${BASE_URL}/books/`)
  .then(response => response.json())
  .then(data => console.log(data));

// Filter by author
fetch(`${BASE_URL}/books/?author=1`)
  .then(response => response.json())
  .then(data => console.log(data));

// Search
fetch(`${BASE_URL}/books/?search=orwell`)
  .then(response => response.json())
  .then(data => console.log(data));

// Order by title
fetch(`${BASE_URL}/books/?ordering=title`)
  .then(response => response.json())
  .then(data => console.log(data));

// Combined query
const params = new URLSearchParams({
  author: 1,
  search: 'orwell',
  ordering: '-publication_year'
});
fetch(`${BASE_URL}/books/?${params}`)
  .then(response => response.json())
  .then(data => console.log(data));
```

## Implementation Details

### View Configuration

The filtering, searching, and ordering capabilities are implemented in the `BookListView` class:

```python
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    # Filter backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Filtering configuration
    filterset_fields = ['title', 'author', 'publication_year']
    
    # Searching configuration
    search_fields = ['title', 'author__name']
    
    # Ordering configuration
    ordering_fields = ['title', 'publication_year', 'id']
    ordering = ['-publication_year', 'title']  # Default ordering
```

### Filter Backends

1. **DjangoFilterBackend**: Provides filtering by exact field matches
   - Uses `django-filter` package
   - Configured via `filterset_fields`

2. **SearchFilter**: Provides text search across multiple fields
   - Built into Django REST Framework
   - Configured via `search_fields`
   - Performs case-insensitive partial matching

3. **OrderingFilter**: Provides sorting capabilities
   - Built into Django REST Framework
   - Configured via `ordering_fields`
   - Default ordering specified via `ordering`

### Database Optimization

The view uses `select_related('author')` to optimize database queries:

```python
def get_queryset(self):
    return Book.objects.select_related('author')
```

This reduces the number of database queries when accessing author information for each book.

### Field Lookups

- **Direct fields**: `title`, `publication_year` - accessed directly
- **Related fields**: `author__name` - accessed via foreign key relationship using double underscore notation

### Query Parameter Processing

All query parameters are processed automatically by the filter backends:
- Filtering parameters are extracted and applied to the queryset
- Search terms are applied across all `search_fields`
- Ordering parameters override the default ordering

### Error Handling

- Invalid filter values return empty results (no error)
- Invalid ordering fields are ignored
- Search with no matches returns an empty list
- All operations are safe and won't cause server errors

## Best Practices

1. **Use filtering for exact matches**: When you know the exact value
2. **Use searching for text queries**: When you want to find partial matches
3. **Use ordering for sorting**: When you need results in a specific order
4. **Combine features wisely**: Use multiple features together for powerful queries
5. **Consider performance**: Filtering is faster than searching for exact matches
6. **Use appropriate fields**: Order by indexed fields for better performance

## Troubleshooting

### No Results Returned

- Check if filter values match exactly (filtering is case-sensitive for exact matches)
- Verify that the data exists in the database
- Try using search instead of filtering for partial matches

### Search Not Working

- Ensure you're using the `search` parameter (not `q` or other names)
- Check that the search term appears in the searchable fields
- Remember that search is case-insensitive

### Ordering Not Working

- Verify the field name is in `ordering_fields`
- Check for typos in the field name
- Use `-` prefix for descending order

### Performance Issues

- Use filtering instead of searching when possible (filtering is faster)
- Limit the number of results if needed (consider pagination)
- Order by indexed fields for better performance

## Additional Resources

- [Django REST Framework Filtering](https://www.django-rest-framework.org/api-guide/filtering/)
- [Django Filter Documentation](https://django-filter.readthedocs.io/)
- [Django REST Framework Search](https://www.django-rest-framework.org/api-guide/filtering/#searchfilter)
- [Django REST Framework Ordering](https://www.django-rest-framework.org/api-guide/filtering/#orderingfilter)

---

**Last Updated**: 2024
**Project**: advanced-api-project
**API Endpoint**: `/api/books/`

