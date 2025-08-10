from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

# List all authors and their books
class AuthorListView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

# List all books or create a new one
class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer