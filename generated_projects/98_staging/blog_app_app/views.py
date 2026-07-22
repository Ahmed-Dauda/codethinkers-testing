from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm

class PostListView(ListView):
    model = Post
    template_name = 'list.html'
    paginate_by = 25

class PostDetailView(DetailView):
    model = Post
    template_name = 'detail.html'

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create.html'
    success_url = reverse_lazy('post_list')

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'update.html'
    success_url = reverse_lazy('post_list')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('post_list')
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
    success_url = reverse_lazy('blog_app_app:comment_list')

class CommentUpdateView(UpdateView):
    template_name = 'comment_form.html'
    model = Comment
    form_class = CommentForm
    success_url = reverse_lazy('blog_app_app:comment_list')

class CommentDeleteView(DeleteView):
    template_name = 'comment_confirm_delete.html'
    model = Comment
    success_url = reverse_lazy('blog_app_app:comment_list')
