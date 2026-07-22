from django.contrib import admin
from .models import Income, Expense, Category

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
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25

@admin.register(Income)
class IncomeAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ['amount', 'date', 'category']
    list_filter = ['date', 'category']
    search_fields = ['amount']
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25

@admin.register(Expense)
class ExpenseAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ['amount', 'date', 'category']
    list_filter = ['date', 'category']
    search_fields = ['amount']
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25