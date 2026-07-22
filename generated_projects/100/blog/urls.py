from django.urls import path
from . import views

urlpatterns = [
    path('', views.BlogPostListView.as_view(), name='blogpost_list'),
    path('post/<int:pk>/', views.BlogPostDetailView.as_view(), name='blogpost_detail'),
]