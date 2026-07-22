from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import BlogPost, Comment

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'list.html'
    paginate_by = 25

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'detail.html'

class BlogPostCreateView(CreateView):
    model = BlogPost
    template_name = 'create.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('blog_post_list')

class BlogPostUpdateView(UpdateView):
    model = BlogPost
    template_name = 'update.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('blog_post_list')

class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'delete.html'
    success_url = reverse_lazy('blog_post_list')
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
