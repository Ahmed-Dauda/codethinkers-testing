from django.urls import path
from . import views

urlpatterns = [
    path('', views.BlogPostListView.as_view(), name='blog_post_list'),
    path('post/<int:pk>/', views.BlogPostDetailView.as_view(), name='blog_post_detail'),
    path('post/create/', views.BlogPostCreateView.as_view(), name='blog_post_create'),
    path('post/update/<int:pk>/', views.BlogPostUpdateView.as_view(), name='blog_post_update'),
    path('post/delete/<int:pk>/', views.BlogPostDeleteView.as_view(), name='blog_post_delete'),
    path('blogpost/', views.BlogPostListView.as_view(), name='blogpost_list'),
    path('blogpost/<int:pk>/', views.BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('blogpost/create/', views.BlogPostCreateView.as_view(), name='blogpost_create'),
    path('blogpost/<int:pk>/update/', views.BlogPostUpdateView.as_view(), name='blogpost_update'),
    path('blogpost/<int:pk>/delete/', views.BlogPostDeleteView.as_view(), name='blogpost_delete'),

]