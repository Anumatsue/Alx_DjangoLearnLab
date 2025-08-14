from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    Serializes all fields of the Book model.
    Includes validation to ensure the publication_year is not in the future.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        Ensure publication year is not greater than the current year.
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes the Author model, including a nested list of books.
    The 'books' field is read-only and populated using BookSerializer.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']