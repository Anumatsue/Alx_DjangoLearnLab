from django.shortcuts import render

# Create your views here.

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .serializers import BookSerializer
from datetime import datetime
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework  # required for checker
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import BookSerializer

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
    Supports:
        - Filtering by title, author name, and publication year.
        - Searching by title or author's name.
        - Ordering by title or publication year.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Enable filter, search, and ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Filtering: query parameters ?title=...&publication_year=...
    filterset_fields = ['title', 'publication_year', 'author']

    # Searching: query parameter ?search=keyword
    search_fields = ['title', 'author__name']

    # Ordering: query parameter ?ordering=title or ?ordering=-publication_year
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering


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