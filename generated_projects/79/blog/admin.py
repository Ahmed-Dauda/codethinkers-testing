from django.contrib import admin
from .models import Post, Category, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'image')
    search_fields = ('title', 'content')
    list_filter = ('category',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'post', 'created_at')
    search_fields = ('content',)