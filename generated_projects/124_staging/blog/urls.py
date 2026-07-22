from django.urls import path
from .views import BlogPostListView, BlogPostDetailView, BlogPostCreateView

app_name = 'blog'

urlpatterns = [
    path('', BlogPostListView.as_view(), name='blogpost_list'),
    path('<int:pk>/', BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('create/', BlogPostCreateView.as_view(), name='blogpost_create'),
]