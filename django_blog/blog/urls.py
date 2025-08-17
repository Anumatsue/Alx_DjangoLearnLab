from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    BlogLoginView, BlogLogoutView, register, profile,  # from your auth work
)

urlpatterns = [
    # Auth (already added earlier)
    path("login/",   BlogLoginView.as_view(), name="login"),
    path("logout/",  BlogLogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),
    path("profile/",  profile, name="profile"),

    # Posts
    path("", PostListView.as_view(), name="post-list"),  # homepage shows posts
    path("posts/", PostListView.as_view(), name="post-list"),  # optional duplicate
    path("posts/new/", PostCreateView.as_view(), name="post-create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/edit/", PostUpdateView.as_view(), name="post-edit"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
]