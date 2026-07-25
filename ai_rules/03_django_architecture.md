# Django Architecture Rules

## Templates
- **home.html is MANDATORY** — every project MUST include a home.html template with dashboard stats AND a root URL: `path('', HomeView.as_view(), name='home')`. The root URL must be the FIRST pattern in urlpatterns. A project without a working `/` URL is INCOMPLETE.

- EVERY view MUST have `template_name = 'xxx.html'` as the FIRST line in the class body
- Template names MUST be model-specific: `post_list.html` NOT `list.html`. Always prefix with the lowercase model name.
- Template paths MUST be bare filenames: `'post_list.html'` NOT `'app_name/post_list.html'`

## Models (models_py)
- At least ONE model with real fields. Add __str__, Meta ordering, timestamps.
- ⚠️ MANDATORY: Every field used in `list_filter`, `list_display`, `search_fields`, `order_by()`, `.filter()`, or `.order_by()` MUST have `db_index=True`. This includes:
  - All ForeignKey fields (Django auto-indexes these, but still list them)
  - All DateField/DateTimeField fields
  - All CharField fields used in search_fields
  - All BooleanField fields used in list_filter
  - All choice/status fields
  Example: `title = models.CharField(max_length=200, db_index=True)`
- Use appropriate field types (ImageField needs Pillow).

## Views (views_py)
- Generate views based on what the user requested. If they said "read-only blog", only ListView + DetailView. If they said "full CRUD", generate all five. If they said "admin only", skip public views entirely. Let the user's prompt decide.
- Every ListView MUST set `paginate_by = 25`
- `.select_related()` for FK fields shown in templates
- `.prefetch_related()` for M2M/reverse FK
- `success_url` on every CreateView/UpdateView/DeleteView
- `.order_by('-id')` on ALL QuerySets

## Admin (admin_py)

### Required Imports (ALWAYS include these)
```python
from django.contrib import admin
from django.http import HttpResponse
import csv
from docx import Document
```

### ExportAdminMixin (ALWAYS define once at top of admin.py)
```python
class ExportAdminMixin:
    actions = ['export_as_csv', 'export_as_docx']

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural}.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset.select_related().iterator(chunk_size=1000):
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
        for obj in queryset.select_related().iterator(chunk_size=1000):
            row_cells = table.add_row().cells
            for i, name in enumerate(field_names):
                row_cells[i].text = str(getattr(obj, name))
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural}.docx'
        document.save(response)
        return response
    export_as_docx.short_description = "Export selected as Word document"
```
⚠️ CRITICAL: `admin.py` MUST import every model it registers. The FIRST line after the imports should be:
```python
from .models import ModelName1, ModelName2, ModelName3

### Every ModelAdmin MUST include ALL of these:
```python
@admin.register(ModelName)
class ModelNameAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ('field1', 'field2', 'field3')      # 3-5 useful fields
    list_filter = ('fk_field', 'date_field', 'bool_field')  # Every FK, Date, Boolean, choice
    search_fields = ('name', 'email', 'fk__name')      # Text fields + FK lookups with __
    list_per_page = 25                                  # REQUIRED - never skip
    readonly_fields = ('created_at', 'updated_at')      # For all timestamp fields
    list_select_related = ('fk_field1', 'fk_field2')    # EVERY FK in list_display/list_filter
    autocomplete_fields = ('fk_field',)                 # FKs to models with search_fields
    date_hierarchy = 'date_field'                       # If model has a date field
    ordering = ('-id',)                                 # Match Meta.ordering

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('fk_field1', 'fk_field2').order_by('-id')