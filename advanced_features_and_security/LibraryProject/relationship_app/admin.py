from django.contrib import admin
from .models import Author, Book, Library, Librarian, UserProfile

# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author')
    list_filter = ('author',)
    search_fields = ('title', 'author__name')


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    filter_horizontal = ('books',)  # Better UI for ManyToMany fields
    search_fields = ('name',)


@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'library')
    list_filter = ('library',)
    search_fields = ('name', 'library__name')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'role')
