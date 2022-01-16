from django.contrib import admin
from sms.models import Categories, Courses, Topics, Comment, course_links
# from users.models import Profile
# Register your models here.

@admin.register(course_links)
class courseurladmin(admin.ModelAdmin):
    # list_display = ['id', 'name', 'desc', 'created']
    # list_filter = ordering = ['created']
    ordering = ['created'] 

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
    ordering = ['created']


# @admin.register(Profile)
# class userprofileadmin(admin.ModelAdmin):
# #     list_display = ['id', 'name', 'desc', 'created']
#     ordering = ['created']



