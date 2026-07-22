from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    paginate_by = 25

    def get_queryset(self):
        return Post.objects.select_related('author').order_by('-created_at')

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_queryset(self):
        return Post.objects.select_related('author')

class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = ['title', 'content']
    success_url = '/'

    def get_queryset(self):
        return Post.objects.select_related('author')

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title', 'content']
    success_url = '/'

    def get_queryset(self):
        return Post.objects.select_related('author')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = '/' 

    def get_queryset(self):
        return Post.objects.select_related('author')