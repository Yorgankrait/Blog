from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    FavoritePostsView,
)
from . import views

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', views.add_comment, name='add-comment'),
    path('post/<int:pk>/like/', views.like_post, name='like-post'),
    path('post/<int:pk>/dislike/', views.dislike_post, name='dislike-post'),
    path('post/<int:pk>/favorite/', views.toggle_favorite, name='toggle-favorite'),
    path('favorites/', FavoritePostsView.as_view(), name='favorites'),
] 