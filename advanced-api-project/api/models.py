from django.db import models

# Create your models here.
class Author(models.Model):
    """
    Represents an author who can have multiple books.
    Fields:
        - name: The author's full name (string).
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Represents a book written by an author.
    Fields:
        - title: The book's title.
        - publication_year: Year the book was published.
        - author: ForeignKey to Author (One-to-Many relationship).
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"