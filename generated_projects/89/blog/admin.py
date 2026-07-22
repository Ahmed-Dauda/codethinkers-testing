from django.contrib import admin
from .models import Post, Category, Comment

class ExportAdminMixin:
    actions = ['export_as_csv', 'export_as_docx']

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
    export_as_csv.short_description = "Export selected as CSV"

    def export_as_docx(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        document = Document()
        document.add_heading(str(meta.verbose_name_plural).title(), level=1)
        table = document.add_table(rows=1, cols=len(field_names))
        table.style = 'Light Grid Accent 1'
        hdr_cells = table.rows[0].cells
        for i, name in enumerate(field_names):
            hdr_cells[i].text = name
        for obj in queryset:
            row_cells = table.add_row().cells
            for i, name in enumerate(field_names):
                row_cells[i].text = str(getattr(obj, name))
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural}.docx'
        document.save(response)
        return response
    export_as_docx.short_description = "Export selected as Word document"

@admin.register(Category)
class CategoryAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['name']
    list_per_page = 25
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Post)
class PostAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'created_at']
    list_filter = ['author', 'category', 'created_at']
    search_fields = ['title', 'content']
    list_per_page = 25
    readonly_fields = ('created_at', 'updated_at')
    list_select_related = ('author', 'category')

@admin.register(Comment)
class CommentAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ['post', 'name', 'email', 'created_at']
    list_filter = ['post', 'created_at']
    search_fields = ['name', 'email', 'content']
    list_per_page = 25
    readonly_fields = ('created_at',)
    list_select_related = ('post',)