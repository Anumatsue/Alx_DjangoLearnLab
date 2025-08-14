from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from .models import Author, Book


class BookAPITests(TestCase):
    """
    Comprehensive tests for Book endpoints:
    - Permissions (read-only for unauth, write for authenticated)
    - CRUD (list, detail, create, update, delete)
    - Filtering (?title= / ?publication_year= / ?author=)
    - Searching (?search=)
    - Ordering (?ordering=title / ?ordering=-publication_year)
    """

    def setUp(self):
        # API client
        self.client = APIClient()

        # Users
        from django.contrib.auth.models import User
        self.user = User.objects.create_user(username="alice", password="password123")

        # Authors
        self.author1 = Author.objects.create(name="George Orwell")
        self.author2 = Author.objects.create(name="Robert C. Martin")

        # Books
        self.book1 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author1,
        )
        self.book2 = Book.objects.create(
            title="Animal Farm",
            publication_year=1945,
            author=self.author1,
        )
        self.book3 = Book.objects.create(
            title="Clean Code",
            publication_year=2008,
            author=self.author2,
        )

        # URL names from api/urls.py
        self.list_url = reverse("book-list")                      # /books/
        self.create_url = reverse("book-create")                  # /books/create/
        self.detail_url = reverse("book-detail", args=[self.book1.pk])     # /books/<pk>/
        self.update_url = reverse("book-update", args=[self.book1.pk])     # /books/update/<pk>/
        self.delete_url = reverse("book-delete", args=[self.book2.pk])     # /books/delete/<pk>/

    # ---------------------------
    # Permissions: read-only for unauthenticated
    # ---------------------------
    def test_unauthenticated_can_list_and_retrieve(self):
        # List
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resp.json()), 3)

        # Detail
        resp = self.client.get(self.detail_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()["id"], self.book1.id)

    def test_unauthenticated_cannot_create_update_delete(self):
        # Create
        resp = self.client.post(self.create_url, {
            "title": "Unauthorized Book",
            "publication_year": 2020,
            "author": self.author1.id
        }, format="json")
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # Update
        resp = self.client.patch(self.update_url, {"title": "Hacked"}, format="json")
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # Delete
        resp = self.client.delete(self.delete_url)
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    # ---------------------------
    # Authenticated: full CRUD
    # ---------------------------
    def test_authenticated_create_book(self):
        self.client.login(username="alice", password="password123")
        resp = self.client.post(self.create_url, {
            "title": "The Clean Coder",
            "publication_year": 2011,
            "author": self.author2.id
        }, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.json()
        self.assertEqual(data["title"], "The Clean Coder")
        self.assertEqual(data["publication_year"], 2011)
        self.assertEqual(data["author"], self.author2.id)
        self.assertTrue(Book.objects.filter(title="The Clean Coder").exists())

    def test_authenticated_update_book(self):
        self.client.login(username="alice", password="password123")
        resp = self.client.patch(self.update_url, {
            "title": "Nineteen Eighty-Four"
        }, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Nineteen Eighty-Four")

    def test_authenticated_delete_book(self):
        self.client.login(username="alice", password="password123")
        resp = self.client.delete(self.delete_url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book2.pk).exists())

    # ---------------------------
    # Validation
    # ---------------------------
    def test_create_book_rejects_future_publication_year(self):
        self.client.login(username="alice", password="password123")
        next_year = timezone.now().year + 1
        resp = self.client.post(self.create_url, {
            "title": "Future Book",
            "publication_year": next_year,
            "author": self.author1.id
        }, format="json")
        # Should be a serializer validation error -> 400
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", resp.json())

    # ---------------------------
    # Filtering / Searching / Ordering
    # ---------------------------
    def test_filter_by_title(self):
        resp = self.client.get(self.list_url, {"title": "Clean Code"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        results = resp.json()
        # Depending on pagination, results may be list or dict with 'results'
        items = results if isinstance(results, list) else results.get("results", [])
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "Clean Code")

    def test_filter_by_publication_year(self):
        resp = self.client.get(self.list_url, {"publication_year": 1949})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        items = resp.json() if isinstance(resp.json(), list) else resp.json().get("results", [])
        self.assertTrue(all(b["publication_year"] == 1949 for b in items))

    def test_filter_by_author_id(self):
        resp = self.client.get(self.list_url, {"author": self.author1.id})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        items = resp.json() if isinstance(resp.json(), list) else resp.json().get("results", [])
        # Only Orwell's books
        self.assertTrue(all(Book.objects.get(pk=b["id"]).author_id == self.author1.id for b in items))

    def test_search_by_title_and_author_name(self):
        # Search "Clean" should match "Clean Code"
        resp = self.client.get(self.list_url, {"search": "Clean"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        items = resp.json() if isinstance(resp.json(), list) else resp.json().get("results", [])
        self.assertTrue(any(b["title"] == "Clean Code" for b in items))

        # Search "Orwell" should match Orwell's books via author__name
        resp = self.client.get(self.list_url, {"search": "Orwell"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        items = resp.json() if isinstance(resp.json(), list) else resp.json().get("results", [])
        titles = {b["title"] for b in items}
        self.assertTrue({"1984", "Animal Farm"}.issubset(titles))

    def test_ordering_by_title_and_publication_year(self):
        # Asc by title
        resp = self.client.get(self.list_url, {"ordering": "title"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        items = resp.json() if isinstance(resp.json(), list) else resp.json().get("results", [])
        titles = [b["title"] for b in items]
        self.assertEqual(titles, sorted(titles))

        # Desc by year
        resp = self.client.get(self.list_url, {"ordering": "-publication_year"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        items = resp.json() if isinstance(resp.json(), list) else resp.json().get("results", [])
        years = [b["publication_year"] for b in items]
        self.assertEqual(years, sorted(years, reverse=True))