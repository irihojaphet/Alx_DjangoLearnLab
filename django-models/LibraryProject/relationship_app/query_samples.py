"""
Sample queries demonstrating Django ORM relationships:
- ForeignKey (Author -> Book)
- ManyToMany (Library -> Book)
- OneToOne (Library -> Librarian)

This script can be run in Django shell using:
python manage.py shell < query_samples.py
Or copy and paste these queries into the Django shell.
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def query_books_by_author():
    """
    Query 1: Query all books by a specific author.
    Demonstrates ForeignKey relationship (reverse lookup).
    """
    print("=" * 60)
    print("QUERY 1: Query all books by a specific author")
    print("=" * 60)
    
    # Method 1: Get author by name and access books through related_name
    author_name = "J.K. Rowling"  # Replace with actual author name in your database
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()  # Using related_name='books'
        
        print(f"\nBooks by {author_name}:")
        if books:
            for book in books:
                print(f"  - {book.title}")
        else:
            print(f"  No books found for {author_name}")
    except Author.DoesNotExist:
        print(f"  Author '{author_name}' not found in database")
        print("  Note: Create an author and books first to see results")
    
    # Method 2: Filter books directly by author
    print("\nAlternative method - Filter books directly:")
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        for book in books:
            print(f"  - {book.title}")
    except Author.DoesNotExist:
        print(f"  Author '{author_name}' not found")
    
    # Method 3: Filter books by author name
    print("\nAlternative method - Filter by author name:")
    books = Book.objects.filter(author__name=author_name)
    if books:
        for book in books:
            print(f"  - {book.title}")
    else:
        print(f"  No books found for author '{author_name}'")
    
    print()


def query_books_in_library():
    """
    Query 2: List all books in a library.
    Demonstrates ManyToMany relationship.
    """
    print("=" * 60)
    print("QUERY 2: List all books in a library")
    print("=" * 60)
    
    library_name = "Central Library"  # Replace with actual library name in your database
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()  # Access books through ManyToMany relationship
        
        print(f"\nBooks in {library_name}:")
        if books:
            for book in books:
                print(f"  - {book.title} (by {book.author.name})")
        else:
            print(f"  No books found in {library_name}")
    except Library.DoesNotExist:
        print(f"  Library '{library_name}' not found in database")
        print("  Note: Create a library and add books to it first to see results")
    
    # Alternative: Count books in library
    print("\nAlternative method - Count books:")
    try:
        library = Library.objects.get(name=library_name)
        book_count = library.books.count()
        print(f"  Total books in {library_name}: {book_count}")
    except Library.DoesNotExist:
        print(f"  Library '{library_name}' not found")
    
    # Alternative: Get libraries that have a specific book
    print("\nAlternative - Find libraries containing a specific book:")
    try:
        book = Book.objects.first()
        if book:
            libraries = book.libraries.all()  # Reverse lookup using related_name='libraries'
            print(f"  Libraries containing '{book.title}':")
            for lib in libraries:
                print(f"    - {lib.name}")
        else:
            print("  No books found in database")
    except Exception as e:
        print(f"  Error: {e}")
    
    print()


def query_librarian_for_library():
    """
    Query 3: Retrieve the librarian for a library.
    Demonstrates OneToOne relationship.
    """
    print("=" * 60)
    print("QUERY 3: Retrieve the librarian for a library")
    print("=" * 60)
    
    library_name = "Central Library"  # Replace with actual library name in your database
    try:
        library = Library.objects.get(name=library_name)
        
        # Method 1: Access librarian through related_name (reverse lookup)
        try:
            librarian = library.librarian  # Using related_name='librarian'
            print(f"\nLibrarian for {library_name}:")
            print(f"  Name: {librarian.name}")
        except Librarian.DoesNotExist:
            print(f"  No librarian assigned to {library_name}")
            print("  Note: Create a librarian for this library first to see results")
    except Library.DoesNotExist:
        print(f"  Library '{library_name}' not found in database")
    
    # Method 2: Get librarian directly
    print("\nAlternative method - Get librarian directly:")
    try:
        librarian = Librarian.objects.get(library__name=library_name)
        print(f"  Librarian: {librarian.name}")
        print(f"  Library: {librarian.library.name}")
    except Librarian.DoesNotExist:
        print(f"  No librarian found for library '{library_name}'")
    
    # Method 3: Check if library has a librarian
    print("\nAlternative method - Check if library has librarian:")
    try:
        library = Library.objects.get(name=library_name)
        if hasattr(library, 'librarian'):
            print(f"  {library_name} has librarian: {library.librarian.name}")
        else:
            print(f"  {library_name} does not have a librarian assigned")
    except Library.DoesNotExist:
        print(f"  Library '{library_name}' not found")
    
    print()


def create_sample_data():
    """
    Helper function to create sample data for testing queries.
    Run this first if you want to test the queries with actual data.
    """
    print("=" * 60)
    print("Creating sample data...")
    print("=" * 60)
    
    # Create authors
    author1, created = Author.objects.get_or_create(name="J.K. Rowling")
    if created:
        print(f"Created author: {author1.name}")
    else:
        print(f"Author already exists: {author1.name}")
    
    author2, created = Author.objects.get_or_create(name="George Orwell")
    if created:
        print(f"Created author: {author2.name}")
    else:
        print(f"Author already exists: {author2.name}")
    
    # Create books
    book1, created = Book.objects.get_or_create(title="Harry Potter and the Philosopher's Stone", author=author1)
    if created:
        print(f"Created book: {book1.title}")
    
    book2, created = Book.objects.get_or_create(title="1984", author=author2)
    if created:
        print(f"Created book: {book2.title}")
    
    book3, created = Book.objects.get_or_create(title="Animal Farm", author=author2)
    if created:
        print(f"Created book: {book3.title}")
    
    # Create library
    library, created = Library.objects.get_or_create(name="Central Library")
    if created:
        print(f"Created library: {library.name}")
    
    # Add books to library (ManyToMany)
    library.books.add(book1, book2, book3)
    print(f"Added books to {library.name}")
    
    # Create librarian (OneToOne)
    librarian, created = Librarian.objects.get_or_create(
        name="Jane Smith",
        library=library
    )
    if created:
        print(f"Created librarian: {librarian.name} for {library.name}")
    else:
        print(f"Librarian already exists: {librarian.name}")
    
    print("\nSample data created successfully!")
    print()


if __name__ == "__main__":
    # Uncomment the line below to create sample data first
    # create_sample_data()
    
    # Run the queries
    query_books_by_author()
    query_books_in_library()
    query_librarian_for_library()
    
    print("=" * 60)
    print("All queries completed!")
    print("=" * 60)
    print("\nTo use these queries in Django shell:")
    print("1. Run: python manage.py shell")
    print("2. Import: from relationship_app.query_samples import *")
    print("3. Or copy individual query functions and run them")
    print("\nTo create sample data, uncomment create_sample_data() in the script")

