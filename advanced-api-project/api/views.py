from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer


class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all books.
    
    This view handles GET requests to retrieve a list of all books in the database.
    It uses Django REST Framework's ListAPIView which automatically handles:
    - Querying all Book instances
    - Serializing the queryset
    - Returning paginated results (if pagination is configured)
    
    Permissions:
        - Allows unauthenticated users to view the list (read-only access)
        - Uses AllowAny permission class for public read access
    
    Endpoint: GET /api/books/
    
    Response:
        Returns a list of all books with their details (id, title, publication_year, author)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public read access
    
    def get_queryset(self):
        """
        Customize the queryset if needed.
        This method can be extended to add filtering, searching, or ordering.
        
        Returns:
            QuerySet: All Book instances, ordered by publication year (newest first)
        """
        return Book.objects.select_related('author').order_by('-publication_year', 'title')


class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID.
    
    This view handles GET requests to retrieve a specific book by its primary key.
    It uses Django REST Framework's RetrieveAPIView which automatically handles:
    - Looking up the book by ID
    - Serializing the book instance
    - Returning 404 if the book doesn't exist
    
    Permissions:
        - Allows unauthenticated users to view book details (read-only access)
        - Uses AllowAny permission class for public read access
    
    Endpoint: GET /api/books/<int:pk>/
    
    Response:
        Returns a single book with all its details (id, title, publication_year, author)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public read access
    lookup_field = 'pk'  # Default lookup field (can be customized)
    
    def get_queryset(self):
        """
        Optimize queryset by using select_related to reduce database queries.
        
        Returns:
            QuerySet: Book instances with related author data pre-fetched
        """
        return Book.objects.select_related('author')


class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book.
    
    This view handles POST requests to create a new book instance.
    It uses Django REST Framework's CreateAPIView which automatically handles:
    - Validating incoming data using the serializer
    - Creating the book instance if validation passes
    - Returning appropriate error messages if validation fails
    
    Permissions:
        - Requires authentication (only authenticated users can create books)
        - Uses IsAuthenticated permission class
    
    Customization:
        - Overrides perform_create to add custom logic before saving
        - Returns custom response format
    
    Endpoint: POST /api/books/create/
    
    Request Body:
        {
            "title": "Book Title",
            "publication_year": 2023,
            "author": 1
        }
    
    Response:
        Returns the created book with status 201 Created
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires authentication
    
    def perform_create(self, serializer):
        """
        Customize the creation process.
        This method is called after validation but before saving.
        Can be used to add additional logic, set fields, or perform side effects.
        
        Args:
            serializer: The validated BookSerializer instance
        """
        # The serializer's validation (including publication_year check) runs automatically
        # Additional custom logic can be added here if needed
        serializer.save()
    
    def create(self, request, *args, **kwargs):
        """
        Override create method to customize the response.
        This ensures proper handling of form submissions and data validation.
        
        Args:
            request: The HTTP request object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments
        
        Returns:
            Response: Custom response with created book data or validation errors
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'message': 'Book created successfully',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book.
    
    This view handles PUT and PATCH requests to update an existing book.
    It uses Django REST Framework's UpdateAPIView which automatically handles:
    - Looking up the book by ID
    - Validating incoming data using the serializer
    - Updating the book instance if validation passes
    - Returning appropriate error messages if validation fails
    
    Permissions:
        - Requires authentication (only authenticated users can update books)
        - Uses IsAuthenticated permission class
    
    Customization:
        - Overrides perform_update to add custom logic before saving
        - Returns custom response format
        - Supports both PUT (full update) and PATCH (partial update)
    
    Endpoint:
        - PUT /api/books/<int:pk>/update/ (full update)
        - PATCH /api/books/<int:pk>/update/ (partial update)
    
    Request Body:
        {
            "title": "Updated Title",
            "publication_year": 2024,
            "author": 1
        }
    
    Response:
        Returns the updated book with status 200 OK
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires authentication
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        """
        Customize the update process.
        This method is called after validation but before saving.
        Can be used to add additional logic, track changes, or perform side effects.
        
        Args:
            serializer: The validated BookSerializer instance
        """
        # The serializer's validation (including publication_year check) runs automatically
        # Additional custom logic can be added here if needed
        serializer.save()
    
    def update(self, request, *args, **kwargs):
        """
        Override update method to customize the response.
        This ensures proper handling of form submissions and data validation.
        Supports both PUT (full update) and PATCH (partial update).
        
        Args:
            request: The HTTP request object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments
        
        Returns:
            Response: Custom response with updated book data or validation errors
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(
            {
                'message': 'Book updated successfully',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book.
    
    This view handles DELETE requests to remove a book from the database.
    It uses Django REST Framework's DestroyAPIView which automatically handles:
    - Looking up the book by ID
    - Deleting the book instance
    - Returning 404 if the book doesn't exist
    
    Permissions:
        - Requires authentication (only authenticated users can delete books)
        - Uses IsAuthenticated permission class
    
    Customization:
        - Overrides destroy method to return custom response message
    
    Endpoint: DELETE /api/books/<int:pk>/delete/
    
    Response:
        Returns success message with status 204 No Content
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires authentication
    lookup_field = 'pk'
    
    def destroy(self, request, *args, **kwargs):
        """
        Override destroy method to customize the response.
        Provides a more informative response message upon successful deletion.
        
        Args:
            request: The HTTP request object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments
        
        Returns:
            Response: Custom response with deletion confirmation message
        """
        instance = self.get_object()
        book_title = instance.title
        self.perform_destroy(instance)
        return Response(
            {
                'message': f'Book "{book_title}" deleted successfully'
            },
            status=status.HTTP_204_NO_CONTENT
        )
