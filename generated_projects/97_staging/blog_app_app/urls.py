from django.urls import path
from . import views

urlpatterns = [
    path('', views.BlogPostListView.as_view(), name='blog_post_list'),
    path('post/<int:pk>/', views.BlogPostDetailView.as_view(), name='blog_post_detail'),
    path('post/new/', views.BlogPostCreateView.as_view(), name='blog_post_create'),
    path('post/<int:pk>/edit/', views.BlogPostUpdateView.as_view(), name='blog_post_update'),
    path('post/<int:pk>/delete/', views.BlogPostDeleteView.as_view(), name='blog_post_delete'),
    path('blogpost/', views.BlogPostListView.as_view(), name='blogpost_list'),
    path('blogpost/<int:pk>/', views.BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('blogpost/create/', views.BlogPostCreateView.as_view(), name='blogpost_create'),
    path('blogpost/<int:pk>/update/', views.BlogPostUpdateView.as_view(), name='blogpost_update'),
    path('blogpost/<int:pk>/delete/', views.BlogPostDeleteView.as_view(), name='blogpost_delete'),

    path('comment/', views.CommentListView.as_view(), name='comment_list'),
    path('comment/<int:pk>/', views.CommentDetailView.as_view(), name='comment_detail'),
    path('comment/create/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),

]