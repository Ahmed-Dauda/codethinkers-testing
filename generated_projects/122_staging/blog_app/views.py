from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    paginate_by = 25

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('post_list')