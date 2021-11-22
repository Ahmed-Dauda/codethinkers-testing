from django.contrib import admin
from sms.models import Categoriess, Coursess, Topicss, Comments
# Register your models here.

@admin.register(Comments)
class commentadmin(admin.ModelAdmin):
    # list_display = ['id', 'name', 'desc', 'created']
    # list_filter = ordering = ['created']
    ordering = ['created']

@admin.register(Categoriess)
class categoriesadmin(admin.ModelAdmin):
    # list_display = ['id', 'name', 'desc', 'created']
    ordering = ['created']

@admin.register(Coursess)
class coursesadmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'desc', 'created']
    ordering = ['created']

@admin.register(Topicss)
class topicsadmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'desc', 'created']
    ordering = ['created']




