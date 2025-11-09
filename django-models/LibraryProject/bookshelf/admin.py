from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Columns on the list page
    list_display = ("title", "author", "publication_year")
    list_display_links = ("title",)
    list_editable = ("publication_year",)  # inline edit in the list view

    # Filters & search
    list_filter = ("publication_year", "author")
    search_fields = ("title", "author")

    # Optional niceties
    ordering = ("title",)
    list_per_page = 25
    fields = ("title", "author", "publication_year")  # controls the detail form layout
