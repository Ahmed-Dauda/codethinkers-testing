from django.views.generic import ListView, DetailView
from .models import BlogPost

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blogpost_list.html'
    paginate_by = 25

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blogpost_detail.html'