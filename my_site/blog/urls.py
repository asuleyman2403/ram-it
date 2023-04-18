from django.urls import path, include
from .views import (
    MainListView,
    PostListView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    post_detail_page,
    create_posts_answer
)
from . import views

urlpatterns = [
    path('', MainListView.as_view(), name='main_home'),
    path('blog/', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', post_detail_page, name='post-detail'),
    path('post/<int:pk>/create-answer', create_posts_answer, name='create-posts-answer'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
]