# Retrieve the Book

```python
# In Django shell: python manage.py shell
from bookshelf.models import Book

# Retrieve by primary key (adjust 1 if your ID differs)
book = Book.objects.get(pk=1)

# Display all attributes deterministically using values()
print(Book.objects.values().get(pk=book.pk))
# Expected output:
# {'id': 1, 'title': '1984', 'author': 'George Orwell', 'publication_year': 1949}
```
