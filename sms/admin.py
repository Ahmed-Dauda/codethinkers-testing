from django.contrib import admin
from sms.models import (
    Categories, Courses, Topics, 
    Comment, Blog, Blogcomment
    )



class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "desc",)
    prepopulated_fields = {"slug": ("title",)}  # new

admin.site.register(Blog, ArticleAdmin)

@admin.register(Comment)
class commentadmin(admin.ModelAdmin):
    # list_display = ['id', 'name', 'desc', 'created']
    # list_filter = ordering = ['created']
    ordering = ['created']

@admin.register(Categories)
class categoriesadmin(admin.ModelAdmin):
    # list_display = ['id', 'name', 'desc', 'created']
    ordering = ['created']

@admin.register(Courses)
class coursesadmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'desc', 'created']
    ordering = ['created']

@admin.register(Topics)
class topicsadmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'desc', 'created']
    prepopulated_fields = {"slug": ("title",)}
    ordering = ['created']


@admin.register(Blogcomment)
class blogcommentadmin(admin.ModelAdmin):
    list_display = ['id','post','name' ,'content']
    # prepopulated_fields = {"slug": ("title",)}
    list_filter =  ['post','created','name']
    search_fields= ['post','name']
    ordering = ['created']
