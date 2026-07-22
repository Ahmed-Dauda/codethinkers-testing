from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm

# List Posts
def post_list(request):
    posts = Post.objects.all().order_by('-id')
    return render(request, 'list.html', {'posts': posts})

# Post Detail
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-id')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

# Create Post
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'form.html', {'form': form})

# Update Post
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'form.html', {'form': form})

# Delete Post
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'confirm_delete.html', {'post': post})