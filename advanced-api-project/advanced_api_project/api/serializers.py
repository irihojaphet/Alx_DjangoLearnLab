from rest_framework import serializers
from datetime import datetime
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer
    
    Serializes all fields of the Book model for API representation.
    This serializer handles the conversion of Book model instances to
    JSON format and vice versa.
    
    Fields:
        - id: Auto-generated primary key
        - title: The title of the book
        - publication_year: The year the book was published
        - author: Foreign key to the Author model (represented as author ID)
    
    Validation:
        - Custom validation ensures publication_year is not in the future.
          This prevents users from creating books with publication dates
          that haven't occurred yet.
    
    Usage:
        >>> serializer = BookSerializer(data={
        ...     'title': '1984',
        ...     'publication_year': 1949,
        ...     'author': 1
        ... })
        >>> serializer.is_valid()
        True
        >>> serializer.save()
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
        read_only_fields = ['id']  # ID is auto-generated, read-only
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        
        Ensures that the publication year is not in the future.
        This validation is called automatically by DRF when validating
        the serializer data.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If the publication year is in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. "
                f"Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer
    
    Serializes Author model instances with nested book information.
    This serializer includes the author's name and dynamically includes
    all related books using a nested BookSerializer.
    
    Fields:
        - id: Auto-generated primary key
        - name: The name of the author
        - books: A nested list of all books written by this author.
                 This field uses BookSerializer to serialize each related book,
                 creating a nested representation of the one-to-many relationship.
    
    Relationship Handling:
        The relationship between Author and Book is handled through the
        'books' field, which uses the BookSerializer to serialize all
        related Book instances. This creates a nested structure where:
        - When serializing an Author, all their books are included as
          nested objects
        - The books are serialized with all their fields (id, title,
          publication_year, author)
        - This allows for rich, nested API responses that include
          complete information about an author and their works
    
    Usage:
        >>> author = Author.objects.get(id=1)
        >>> serializer = AuthorSerializer(author)
        >>> serializer.data
        {
            'id': 1,
            'name': 'J.K. Rowling',
            'books': [
                {'id': 1, 'title': 'Harry Potter', 'publication_year': 1997, 'author': 1},
                ...
            ]
        }
    """
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
        read_only_fields = ['id']  # ID is auto-generated, read-only
    
    def to_representation(self, instance):
        """
        Customize the serialization output.
        
        This method allows us to control how the Author instance is
        represented in the API response. The nested books are automatically
        included through the 'books' field defined above.
        
        Args:
            instance: The Author model instance to serialize
            
        Returns:
            dict: The serialized representation of the Author
        """
        representation = super().to_representation(instance)
        # The books are already included via the nested BookSerializer
        # This method can be extended to add additional customizations
        return representation

