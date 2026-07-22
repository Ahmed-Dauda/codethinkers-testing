from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
]