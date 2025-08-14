from django.shortcuts import render

# Create your views here.

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .serializers import BookSerializer
from datetime import datetime
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

class AuthorListCreateView(generics.ListCreateAPIView):
    """
    Handles GET (list authors with nested books) and POST (create new author).
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookListCreateView(generics.ListCreateAPIView):
    """
    Handles GET (list books) and POST (create new book).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# api/views.py


# ---------------------
# READ OPERATIONS
# ---------------------

class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all books.
    Read-only for all users (no authentication required).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view books


class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public read access


# ---------------------
# CREATE OPERATION
# ---------------------

class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book.
    Only authenticated users can create.
    Custom validation ensures publication_year is not in the future.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Auth required

    def perform_create(self, serializer):
        """
        Hook to customize save behavior (could set defaults, log, etc.).
        """
        current_year = datetime.now().year
        if serializer.validated_data['publication_year'] > current_year:
            raise ValueError("Publication year cannot be in the future.")
        serializer.save()


# ---------------------
# UPDATE OPERATION
# ---------------------

class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book.
    Only authenticated users can update.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Auth required

    def perform_update(self, serializer):
        """
        Example: Custom update logic could log changes or restrict edits.
        """
        print(f"Updating book: {serializer.instance.title}")
        serializer.save()


# ---------------------
# DELETE OPERATION
# ---------------------

class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book.
    Only authenticated users can delete.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Auth required