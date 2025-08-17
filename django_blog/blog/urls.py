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
]