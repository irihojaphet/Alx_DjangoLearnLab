# Delete the Book

```python
# In Django shell: python manage.py shell
from bookshelf.models import Book

book = Book.objects.get(pk=1)
book.delete()

# Confirm deletion
print(list(Book.objects.values()))
# Expected output:
# []
```
