from django.db import models


class Author(models.Model):
    """
    Author Model
    
    Represents an author in the library system. This model stores basic
    information about authors who have written books.
    
    Fields:
        name (CharField): The full name of the author. This is a required field
                         with a maximum length of 200 characters.
    
    Relationships:
        - One-to-Many with Book: An author can have multiple books.
          This relationship is defined on the Book model through a ForeignKey.
    
    Example:
        >>> author = Author.objects.create(name="J.K. Rowling")
        >>> author.name
        'J.K. Rowling'
    """
    name = models.CharField(
        max_length=200,
        help_text="The full name of the author"
    )
    
    class Meta:
        ordering = ['name']  # Order authors alphabetically by name
        verbose_name = "Author"
        verbose_name_plural = "Authors"
    
    def __str__(self):
        """
        String representation of the Author instance.
        Returns the author's name for easy identification.
        """
        return self.name


class Book(models.Model):
    """
    Book Model
    
    Represents a book in the library system. Each book is associated with
    an author through a foreign key relationship, establishing a one-to-many
    relationship where one author can have many books.
    
    Fields:
        title (CharField): The title of the book. Required field with a
                          maximum length of 200 characters.
        publication_year (IntegerField): The year the book was published.
                                        This field is required and will be
                                        validated to ensure it's not in the future.
        author (ForeignKey): A foreign key relationship to the Author model.
                           This establishes the one-to-many relationship where
                           one author can have multiple books. When an author
                           is deleted, their books will also be deleted (CASCADE).
    
    Relationships:
        - Many-to-One with Author: Each book belongs to one author.
          This is implemented through the ForeignKey field pointing to Author.
          The reverse relationship allows accessing all books by an author
          through author.book_set.all() or author.books.all() if related_name
          is set.
    
    Example:
        >>> author = Author.objects.create(name="George Orwell")
        >>> book = Book.objects.create(
        ...     title="1984",
        ...     publication_year=1949,
        ...     author=author
        ... )
        >>> book.author.name
        'George Orwell'
    """
    title = models.CharField(
        max_length=200,
        help_text="The title of the book"
    )
    publication_year = models.IntegerField(
        help_text="The year the book was published"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',  # Allows accessing books via author.books.all()
        help_text="The author who wrote this book"
    )
    
    class Meta:
        ordering = ['-publication_year', 'title']  # Order by year (newest first), then title
        verbose_name = "Book"
        verbose_name_plural = "Books"
    
    def __str__(self):
        """
        String representation of the Book instance.
        Returns the book title and author name for easy identification.
        """
        return f"{self.title} by {self.author.name}"
