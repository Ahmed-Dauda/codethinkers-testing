from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm, CategoryForm

class PostListView(ListView):
    template_name = 'post_list.html'
    model = Post
    paginate_by = 25

    def get_queryset(self):
        return super().get_queryset().select_related('category').order_by('-id')

class PostDetailView(DetailView):
    template_name = 'post_detail.html'
    model = Post

    def get_queryset(self):
        return super().get_queryset().select_related('category').prefetch_related('comments').order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()  # Add the comment form to the context
        return context

class PostCreateView(CreateView):
    template_name = 'post_form.html'
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog:post_list')

class PostUpdateView(UpdateView):
    template_name = 'post_form.html'
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog:post_list')

class PostDeleteView(DeleteView):
    template_name = 'post_confirm_delete.html'
    model = Post
    success_url = reverse_lazy('blog:post_list')

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
    success_url = reverse_lazy('blog:category_list')

class CategoryUpdateView(UpdateView):
    template_name = 'category_form.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('blog:category_list')

class CategoryDeleteView(DeleteView):
    template_name = 'category_confirm_delete.html'
    model = Category
    success_url = reverse_lazy('blog:category_list')

class CommentListView(ListView):
    template_name = 'comment_list.html'
    model = Comment
    paginate_by = 25
    ordering = ['-created_at']

class CommentDetailView(DetailView):
    template_name = 'comment_detail.html'
    model = Comment

class CommentCreateView(CreateView):
    template_name = 'comment_form.html'
    model = Comment
    form_class = CommentForm
    success_url = reverse_lazy('blog:comment_list')

class CommentUpdateView(UpdateView):
    template_name = 'comment_form.html'
    model = Comment
    form_class = CommentForm
    success_url = reverse_lazy('blog:comment_list')

class CommentDeleteView(DeleteView):
    template_name = 'comment_confirm_delete.html'
    model = Comment
    success_url = reverse_lazy('blog:comment_list')