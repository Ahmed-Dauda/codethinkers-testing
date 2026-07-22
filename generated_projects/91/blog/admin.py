from django.contrib import admin
from .models import Post, Category, Comment
from django.http import HttpResponse
import csv

class ExportAdminMixin:
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural}.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response
    export_as_csv.short_description = 'Export selected as CSV'

@admin.register(Category)
class CategoryAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25

@admin.register(Post)
class PostAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25
    list_select_related = ('category',)

@admin.register(Comment)
class CommentAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ('post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content',)
    readonly_fields = ('created_at',)
    list_per_page = 25
    list_select_related = ('post',)