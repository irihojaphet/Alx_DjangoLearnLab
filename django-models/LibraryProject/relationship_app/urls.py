from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import list_books, LibraryDetailView, CustomLoginView, register

app_name = 'relationship_app'

urlpatterns = [
    # Function-based view: List all books
    path('books/', list_books, name='list_books'),
    
    # Class-based view: Library detail
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    
    # Authentication views
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', register, name='register'),
]