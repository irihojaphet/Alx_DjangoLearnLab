"""
Unit tests for the Book API endpoints.

This module contains comprehensive test cases for testing:
- CRUD operations (Create, Read, Update, Delete)
- Filtering, searching, and ordering functionality
- Permissions and authentication mechanisms
- Response data integrity and status codes
"""
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Book


class BookAPITestCase(APITestCase):
    """
    Base test case class for Book API tests.
    
    Sets up test data including authors and books for use across all test cases.
    Uses Django REST Framework's APITestCase which provides:
    - A test client for making API requests
    - Automatic database transaction rollback after each test
    - Helper methods for authentication
    """
    
    def setUp(self):
        """
        Set up test data before each test method runs.
        Creates test authors, books, and a test user for authentication.
        """
        # Create test authors
        self.author1 = Author.objects.create(name="George Orwell")
        self.author2 = Author.objects.create(name="J.K. Rowling")
        
        # Create test books
        self.book1 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="Animal Farm",
            publication_year=1945,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title="Harry Potter",
            publication_year=1997,
            author=self.author2
        )
        
        # Create test user for authentication
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )


class BookListViewTests(BookAPITestCase):
    """
    Test cases for the BookListView endpoint (GET /api/books/).
    
    Tests include:
    - Listing all books
    - Filtering by title, author, and publication_year
    - Searching by title and author name
    - Ordering by different fields
    - Public access (no authentication required)
    """
    
    def test_list_books_public_access(self):
        """
        Test that unauthenticated users can access the book list.
        Verifies that the endpoint returns 200 OK and includes all books.
        """
        url = reverse('api:book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_list_books_response_data(self):
        """
        Test that the book list response contains correct data structure.
        Verifies that each book in the response has the expected fields.
        """
        url = reverse('api:book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        
        # Check that each book has required fields
        for book in response.data:
            self.assertIn('id', book)
            self.assertIn('title', book)
            self.assertIn('publication_year', book)
            self.assertIn('author', book)
    
    def test_filter_by_title(self):
        """
        Test filtering books by exact title match.
        Verifies that only books with the specified title are returned.
        """
        url = reverse('api:book-list')
        response = self.client.get(url, {'title': '1984'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')
    
    def test_filter_by_author(self):
        """
        Test filtering books by author ID.
        Verifies that only books by the specified author are returned.
        """
        url = reverse('api:book-list')
        response = self.client.get(url, {'author': self.author1.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Verify all returned books belong to author1
        for book in response.data:
            self.assertEqual(book['author'], self.author1.id)
    
    def test_filter_by_publication_year(self):
        """
        Test filtering books by publication year.
        Verifies that only books published in the specified year are returned.
        """
        url = reverse('api:book-list')
        response = self.client.get(url, {'publication_year': 1949})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['publication_year'], 1949)
    
    def test_search_by_title(self):
        """
        Test searching books by title using the search parameter.
        Verifies that books with matching titles are returned.
        """
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': '1984'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')
    
    def test_search_by_author_name(self):
        """
        Test searching books by author name using the search parameter.
        Verifies that books by authors with matching names are returned.
        """
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': 'Orwell'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Verify all returned books are by Orwell
        for book in response.data:
            book_obj = Book.objects.get(id=book['id'])
            self.assertEqual(book_obj.author.name, 'George Orwell')
    
    def test_ordering_by_title_ascending(self):
        """
        Test ordering books by title in ascending order.
        Verifies that books are returned in alphabetical order by title.
        """
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        # Verify ascending order
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))
    
    def test_ordering_by_title_descending(self):
        """
        Test ordering books by title in descending order.
        Verifies that books are returned in reverse alphabetical order.
        """
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': '-title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        # Verify descending order
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))
    
    def test_ordering_by_publication_year_ascending(self):
        """
        Test ordering books by publication year in ascending order.
        Verifies that books are returned from oldest to newest.
        """
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': 'publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        # Verify ascending order by year
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years))
    
    def test_ordering_by_publication_year_descending(self):
        """
        Test ordering books by publication year in descending order.
        Verifies that books are returned from newest to oldest.
        """
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        # Verify descending order by year
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
    
    def test_combined_filter_search_order(self):
        """
        Test combining filtering, searching, and ordering in a single request.
        Verifies that all query parameters work together correctly.
        """
        url = reverse('api:book-list')
        response = self.client.get(url, {
            'author': self.author1.id,
            'search': 'Animal',
            'ordering': 'title'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Animal Farm')


class BookDetailViewTests(BookAPITestCase):
    """
    Test cases for the BookDetailView endpoint (GET /api/books/<int:pk>/).
    
    Tests include:
    - Retrieving a single book by ID
    - Handling non-existent book IDs (404 error)
    - Public access (no authentication required)
    """
    
    def test_retrieve_book_public_access(self):
        """
        Test that unauthenticated users can retrieve a single book.
        Verifies that the endpoint returns 200 OK with correct book data.
        """
        url = reverse('api:book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.book1.id)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
        self.assertEqual(response.data['author'], self.book1.author.id)
    
    def test_retrieve_nonexistent_book(self):
        """
        Test retrieving a book that doesn't exist.
        Verifies that the endpoint returns 404 Not Found.
        """
        url = reverse('api:book-detail', kwargs={'pk': 99999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookCreateViewTests(BookAPITestCase):
    """
    Test cases for the BookCreateView endpoint (POST /api/books/create/).
    
    Tests include:
    - Creating a new book with valid data
    - Authentication requirement
    - Validation of publication_year (not in future)
    - Response data integrity
    """
    
    def test_create_book_requires_authentication(self):
        """
        Test that unauthenticated users cannot create books.
        Verifies that the endpoint returns 401 Unauthorized or 403 Forbidden.
        """
        url = reverse('api:book-create')
        data = {
            'title': 'Test Book',
            'publication_year': 2020,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_create_book_authenticated(self):
        """
        Test creating a book with valid data when authenticated.
        Verifies that the book is created and returned with correct data.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('api:book-create')
        data = {
            'title': 'Test Book',
            'publication_year': 2020,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['title'], 'Test Book')
        self.assertEqual(response.data['data']['publication_year'], 2020)
        self.assertEqual(response.data['data']['author'], self.author1.id)
        self.assertIn('message', response.data)
        
        # Verify book was created in database
        self.assertTrue(Book.objects.filter(title='Test Book').exists())
    
    def test_create_book_validation_future_year(self):
        """
        Test that creating a book with a future publication year is rejected.
        Verifies that the validation error is returned with 400 Bad Request.
        """
        from datetime import datetime
        future_year = datetime.now().year + 1
        
        self.client.force_authenticate(user=self.user)
        url = reverse('api:book-create')
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_create_book_missing_fields(self):
        """
        Test that creating a book with missing required fields is rejected.
        Verifies that validation errors are returned.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('api:book-create')
        data = {
            'title': 'Incomplete Book'
            # Missing publication_year and author
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BookUpdateViewTests(BookAPITestCase):
    """
    Test cases for the BookUpdateView endpoint (PUT/PATCH /api/books/<int:pk>/update/).
    
    Tests include:
    - Updating a book with valid data
    - Authentication requirement
    - Partial updates (PATCH)
    - Full updates (PUT)
    - Validation of publication_year
    """
    
    def test_update_book_requires_authentication(self):
        """
        Test that unauthenticated users cannot update books.
        Verifies that the endpoint returns 401 Unauthorized or 403 Forbidden.
        """
        url = reverse('api:book-update', kwargs={'pk': self.book1.id})
        data = {
            'title': 'Updated Title',
            'publication_year': 1949,
            'author': self.author1.id
        }
        response = self.client.put(url, data, format='json')
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_update_book_put_authenticated(self):
        """
        Test updating a book with PUT (full update) when authenticated.
        Verifies that all fields are updated correctly.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('api:book-update', kwargs={'pk': self.book1.id})
        data = {
            'title': 'Updated 1984',
            'publication_year': 1949,
            'author': self.author1.id
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['title'], 'Updated 1984')
        self.assertIn('message', response.data)
        
        # Verify book was updated in database
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated 1984')
    
    def test_update_book_patch_authenticated(self):
        """
        Test updating a book with PATCH (partial update) when authenticated.
        Verifies that only specified fields are updated.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('api:book-update', kwargs={'pk': self.book1.id})
        data = {
            'title': 'Partially Updated 1984'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['title'], 'Partially Updated 1984')
        
        # Verify book was updated in database
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Partially Updated 1984')
        # Verify other fields remain unchanged
        self.assertEqual(self.book1.publication_year, 1949)
    
    def test_update_book_validation_future_year(self):
        """
        Test that updating a book with a future publication year is rejected.
        Verifies that the validation error is returned.
        """
        from datetime import datetime
        future_year = datetime.now().year + 1
        
        self.client.force_authenticate(user=self.user)
        url = reverse('api:book-update', kwargs={'pk': self.book1.id})
        data = {
            'title': '1984',
            'publication_year': future_year,
            'author': self.author1.id
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_update_nonexistent_book(self):
        """
        Test updating a book that doesn't exist.
        Verifies that the endpoint returns 404 Not Found.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('api:book-update', kwargs={'pk': 99999})
        data = {
            'title': 'Nonexistent Book',
            'publication_year': 2020,
            'author': self.author1.id
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookDeleteViewTests(BookAPITestCase):
    """
    Test cases for the BookDeleteView endpoint (DELETE /api/books/<int:pk>/delete/).
    
    Tests include:
    - Deleting a book
    - Authentication requirement
    - Verifying book is removed from database
    """
    
    def test_delete_book_requires_authentication(self):
        """
        Test that unauthenticated users cannot delete books.
        Verifies that the endpoint returns 401 Unauthorized or 403 Forbidden.
        """
        url = reverse('api:book-delete', kwargs={'pk': self.book1.id})
        response = self.client.delete(url)
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_delete_book_authenticated(self):
        """
        Test deleting a book when authenticated.
        Verifies that the book is deleted and appropriate response is returned.
        """
        book_id = self.book1.id
        self.client.force_authenticate(user=self.user)
        url = reverse('api:book-delete', kwargs={'pk': book_id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn('message', response.data)
        
        # Verify book was deleted from database
        self.assertFalse(Book.objects.filter(id=book_id).exists())
    
    def test_delete_nonexistent_book(self):
        """
        Test deleting a book that doesn't exist.
        Verifies that the endpoint returns 404 Not Found.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('api:book-delete', kwargs={'pk': 99999})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

