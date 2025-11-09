# CRUD Operations for `Book` Model (Django Shell)

This document shows the **commands** and **expected outputs** for Create, Retrieve, Update, and Delete.

---

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


---

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


---

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


---

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

