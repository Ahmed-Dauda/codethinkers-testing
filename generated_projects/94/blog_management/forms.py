from django import forms
from .models import Post, Category, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
