"""
Test script for verifying Author and Book serializers.

This script can be run using Django shell:
    python manage.py shell < test_serializers.py

Or copy and paste the commands into Django shell:
    python manage.py shell
"""

from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer
from datetime import datetime

print("=" * 60)
print("Testing Author and Book Serializers")
print("=" * 60)

# Create test data
print("\n1. Creating test authors...")
author1 = Author.objects.create(name="J.K. Rowling")
author2 = Author.objects.create(name="George Orwell")
print(f"   Created: {author1}")
print(f"   Created: {author2}")

# Create test books
print("\n2. Creating test books...")
book1 = Book.objects.create(
    title="Harry Potter and the Philosopher's Stone",
    publication_year=1997,
    author=author1
)
book2 = Book.objects.create(
    title="1984",
    publication_year=1949,
    author=author2
)
book3 = Book.objects.create(
    title="Animal Farm",
    publication_year=1945,
    author=author2
)
print(f"   Created: {book1}")
print(f"   Created: {book2}")
print(f"   Created: {book3}")

# Test BookSerializer
print("\n3. Testing BookSerializer...")
book_serializer = BookSerializer(book1)
print(f"   Serialized book data:")
print(f"   {book_serializer.data}")

# Test AuthorSerializer with nested books
print("\n4. Testing AuthorSerializer with nested books...")
author_serializer = AuthorSerializer(author2)
print(f"   Serialized author data (with nested books):")
import json
print(json.dumps(author_serializer.data, indent=2))

# Test validation - should fail for future year
print("\n5. Testing validation (future publication year)...")
future_book_data = {
    'title': 'Future Book',
    'publication_year': datetime.now().year + 1,
    'author': author1.id
}
future_book_serializer = BookSerializer(data=future_book_data)
if not future_book_serializer.is_valid():
    print(f"   Validation correctly failed: {future_book_serializer.errors}")
else:
    print("   ERROR: Validation should have failed!")

# Test validation - should pass for valid year
print("\n6. Testing validation (valid publication year)...")
valid_book_data = {
    'title': 'Valid Book',
    'publication_year': 2020,
    'author': author1.id
}
valid_book_serializer = BookSerializer(data=valid_book_data)
if valid_book_serializer.is_valid():
    print("   Validation passed successfully!")
    print(f"   Validated data: {valid_book_serializer.validated_data}")
else:
    print(f"   Validation failed: {valid_book_serializer.errors}")

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)

