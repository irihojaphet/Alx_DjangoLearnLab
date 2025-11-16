from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    path('', views.list_books, name='list_books'),
    path('<int:pk>/', views.book_detail, name='book_detail'),
    path('create/', views.create_book, name='create_book'),
    path('<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('<int:pk>/delete/', views.delete_book, name='delete_book'),
]

