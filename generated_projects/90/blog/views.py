from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    paginate_by = 25

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    paginate_by = 25

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'

class CommentListView(ListView):
    model = Comment
    template_name = 'comment_list.html'
    paginate_by = 25

class CommentDetailView(DetailView):
    model = Comment
    template_name = 'comment_detail.html'