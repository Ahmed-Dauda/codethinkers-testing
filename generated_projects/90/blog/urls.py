from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('comments/', views.CommentListView.as_view(), name='comment_list'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment_detail'),
]