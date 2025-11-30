from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Author model.
    Allows managing authors through Django admin panel.
    """
    list_display = ['id', 'name']
    search_fields = ['name']
    list_filter = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Book model.
    Allows managing books through Django admin panel.
    """
    list_display = ['id', 'title', 'publication_year', 'author']
    list_filter = ['publication_year', 'author']
    search_fields = ['title', 'author__name']
    raw_id_fields = ['author']  # Better UX for foreign key selection
