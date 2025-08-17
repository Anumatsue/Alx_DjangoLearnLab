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
]


urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]


urlpatterns = [
    # existing CRUD paths...
    path('search/', views.search, name='search'),
    path("tags/<str:tag_name>/", views.posts_by_tag, name="posts_by_tag"),
]


