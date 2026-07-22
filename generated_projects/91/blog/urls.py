from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),

    path('comment/', views.CommentListView.as_view(), name='comment_list'),
    path('comment/<int:pk>/', views.CommentDetailView.as_view(), name='comment_detail'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/post/', views.CommentCreateView.as_view(), name='comment_create'),
]