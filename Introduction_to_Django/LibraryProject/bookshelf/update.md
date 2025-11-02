# Update the Book's Title

```python
# In Django shell: python manage.py shell
from bookshelf.models import Book

book = Book.objects.get(pk=1)
book.title = "Nineteen Eighty-Four"
book.save()

print(Book.objects.values().get(pk=book.pk))
# Expected output:
# {'id': 1, 'title': 'Nineteen Eighty-Four', 'author': 'George Orwell', 'publication_year': 1949}
```
