# Create a Book

```python
# In Django shell: python manage.py shell
from bookshelf.models import Book

book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)

# Show what we created
print(book.pk, book.title, book.author, book.publication_year)
# Expected output (id may vary on your machine):
# 1 1984 George Orwell 1949
```
