from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='blogpost_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='blogpost_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='blogpost_create'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='blogpost_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='blogpost_delete'),
]