from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Course, Enrollment, Progress, Enrollment, Progress

class ExportAdminMixin:
    actions = ['export_as_csv']

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
    export_as_csv.short_description = 'Export selected as CSV'

@admin.register(Course)
class CourseAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title',)
    list_per_page = 25

@admin.register(Enrollment)
class EnrollmentAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date')
    list_filter = ('course',)
    search_fields = ('student__username', 'course__title')
    list_per_page = 25
    list_select_related = ('course', 'student')

@admin.register(Progress)
class ProgressAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ('enrollment', 'module_name', 'completed', 'grade')
    list_filter = ('completed',)
    search_fields = ('module_name',)
    list_per_page = 25
    list_select_related = ('enrollment',)