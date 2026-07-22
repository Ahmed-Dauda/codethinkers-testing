from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post

class PostListView(ListView):
    template_name = 'post_list.html'
    model = Post
    paginate_by = 25

    def get_queryset(self):
        return Post.objects.select_related('author').order_by('-created_at')

class PostDetailView(DetailView):
    template_name = 'post_detail.html'
    model = Post

    def get_queryset(self):
        return Post.objects.select_related('author')

class PostCreateView(CreateView):
    template_name = 'post_create.html'
    model = Post
    fields = ['title', 'content']
    success_url = '/'

class PostUpdateView(UpdateView):
    template_name = 'post_update.html'
    model = Post
    fields = ['title', 'content']
    success_url = '/' 

class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    model = Post
    success_url = '/'