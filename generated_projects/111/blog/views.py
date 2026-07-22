from django.views.generic import ListView, DetailView
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    paginate_by = 25

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')