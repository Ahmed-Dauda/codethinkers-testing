from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    paginate_by = 25

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    success_url = '/posts/'

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_update.html'
    success_url = '/posts/'

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = '/posts/'
class CategoryListView(ListView):
    template_name = 'category_list.html'
    model = Category
    paginate_by = 25
    ordering = ['-id']

class CategoryDetailView(DetailView):
    template_name = 'category_detail.html'
    model = Category

class CategoryCreateView(CreateView):
    template_name = 'category_form.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('blog_management:category_list')

class CategoryUpdateView(UpdateView):
    template_name = 'category_form.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('blog_management:category_list')

class CategoryDeleteView(DeleteView):
    template_name = 'category_confirm_delete.html'
    model = Category
    success_url = reverse_lazy('blog_management:category_list')

class CommentListView(ListView):
    template_name = 'comment_list.html'
    model = Comment
    paginate_by = 25
    ordering = ['-id']

class CommentDetailView(DetailView):
    template_name = 'comment_detail.html'
    model = Comment

class CommentCreateView(CreateView):
    template_name = 'comment_form.html'
    model = Comment
    form_class = CommentForm
    success_url = reverse_lazy('blog_management:comment_list')

class CommentUpdateView(UpdateView):
    template_name = 'comment_form.html'
    model = Comment
    form_class = CommentForm
    success_url = reverse_lazy('blog_management:comment_list')

class CommentDeleteView(DeleteView):
    template_name = 'comment_confirm_delete.html'
    model = Comment
    success_url = reverse_lazy('blog_management:comment_list')
