from django.views.generic import ListView, DetailView, CreateView
from .models import BlogPost
from .forms import BlogPostForm

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blogpost_list.html'
    paginate_by = 25

    def get_queryset(self):
        return BlogPost.objects.select_related('author').order_by('-created_at')

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blogpost_detail.html'

    def get_queryset(self):
        return BlogPost.objects.select_related('author')

class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blogpost_form.html'
    success_url = '/blog/'  # Redirect to blog list after creation

    def get_queryset(self):
        return BlogPost.objects.select_related('author')