from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
from django.urls import reverse_lazy

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    paginate_by = 25
    def get_queryset(self):
        return super().get_queryset().select_related('author', 'category').order_by('-created_at')

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    def get_queryset(self):
        return super().get_queryset().select_related('author', 'category')

class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    paginate_by = 25

class CommentListView(ListView):
    model = Comment
    template_name = 'comment_list.html'
    paginate_by = 25
    def get_queryset(self):
        return super().get_queryset().select_related('post')