from django.views.generic import ListView, DetailView
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'list.html'
    paginate_by = 25

    def get_queryset(self):
        return Post.objects.all().select_related().order_by('-created_at')

class PostDetailView(DetailView):
    model = Post
    template_name = 'detail.html'

    def get_queryset(self):
        return Post.objects.all().select_related()