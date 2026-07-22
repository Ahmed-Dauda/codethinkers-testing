from django.contrib import admin
from .models import Student
import csv
from django.http import HttpResponse

class StudentAdmin(admin.ModelAdmin):
    search_fields = ['name']  # Added search functionality

    actions = ['export_to_csv']  # Registering the export action

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="students.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'CA', 'Exam', 'Total'])  # CSV header
        for student in queryset:
            writer.writerow([student.name, student.ca, student.exam, student.total])  # CSV data
        return response

    export_to_csv.short_description = 'Export Selected Students to CSV'  # Action description

admin.site.register(Student, StudentAdmin)

admin.site.site_header = 'Administration'
admin.site.site_title = 'Grades Admin'
admin.site.index_title = 'Welcome to the Grades Admin Panel'