from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import BlogPost
from .forms import BlogPostForm

class PostListView(ListView):
    model = BlogPost
    template_name = 'blogpost_list.html'
    paginate_by = 25
    ordering = ['-created_at']

class PostDetailView(DetailView):
    model = BlogPost
    template_name = 'blogpost_detail.html'

class PostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blogpost_form.html'
    success_url = reverse_lazy('blogpost_list')

class PostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blogpost_form.html'
    success_url = reverse_lazy('blogpost_list')

class PostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blogpost_confirm_delete.html'
    success_url = reverse_lazy('blogpost_list')