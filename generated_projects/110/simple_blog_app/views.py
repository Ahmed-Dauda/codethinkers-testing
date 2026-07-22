from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm

class PostListView(ListView):
    template_name = 'post_list.html'
    model = Post
    paginate_by = 25

    def get_queryset(self):
        return Post.objects.order_by('-created_at')

class PostDetailView(DetailView):
    template_name = 'post_detail.html'
    model = Post

class PostCreateView(CreateView):
    template_name = 'post_create.html'
    model = Post
    form_class = PostForm
    success_url = '/posts/'  # Adjust as needed

class PostUpdateView(UpdateView):
    template_name = 'post_update.html'
    model = Post
    form_class = PostForm
    success_url = '/posts/'  # Adjust as needed

class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    model = Post
    success_url = '/posts/'  # Adjust as needed