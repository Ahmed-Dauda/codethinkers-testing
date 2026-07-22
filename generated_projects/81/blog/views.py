from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, content=content)
        return HttpResponseRedirect(self.get_object().get_absolute_url())

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'category']
    template_name = 'post_form.html'
    success_url = reverse_lazy('blog:post_list')

class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'category']
    template_name = 'post_form.html'
    success_url = reverse_lazy('blog:post_list')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')