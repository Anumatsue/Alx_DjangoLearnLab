from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


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