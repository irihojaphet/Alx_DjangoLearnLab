from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on Book model.
    Requires authentication token for all operations.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
