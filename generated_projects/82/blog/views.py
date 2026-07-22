from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment, Tag
from django.urls import reverse_lazy

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = ['-id']

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

class PostCreateView(CreateView):
    model = Post
    template_name = 'post_form.html'
    fields = '__all__'
    success_url = reverse_lazy('blog:post_list')

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_form.html'
    fields = '__all__'
    success_url = reverse_lazy('blog:post_list')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

class TagListView(ListView):
    model = Post
    template_name = 'tag_detail.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(tags__name=self.kwargs['tag_name']).order_by('-id')