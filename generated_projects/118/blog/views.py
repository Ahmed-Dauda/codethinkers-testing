from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost
from .forms import BlogPostForm

class BlogPostListView(ListView):
    template_name = 'blogpost_list.html'
    model = BlogPost
    paginate_by = 25

    def get_queryset(self):
        return BlogPost.objects.select_related('author').order_by('-created_at')

class BlogPostDetailView(DetailView):
    template_name = 'blogpost_detail.html'
    model = BlogPost

    def get_queryset(self):
        return BlogPost.objects.select_related('author')

class BlogPostCreateView(CreateView):
    template_name = 'blogpost_form.html'
    model = BlogPost
    form_class = BlogPostForm
    success_url = '/'

class BlogPostUpdateView(UpdateView):
    template_name = 'blogpost_form.html'
    model = BlogPost
    form_class = BlogPostForm
    success_url = '/'

class BlogPostDeleteView(DeleteView):
    template_name = 'blogpost_confirm_delete.html'
    model = BlogPost
    success_url = '/'