from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogPostListView.as_view(), name='blogpost_list'),
    path('post/<int:pk>/', views.BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('post/create/', views.BlogPostCreateView.as_view(), name='blogpost_create'),
]