from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost
from django.urls import reverse_lazy

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