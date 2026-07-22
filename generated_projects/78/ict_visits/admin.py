from django.contrib import admin
from .models import StudentVisit

class StudentVisitAdmin(admin.ModelAdmin):
    search_fields = ['student_name', 'purpose']  # Enable search by student name and purpose

admin.site.register(StudentVisit, StudentVisitAdmin)

admin.site.site_header = 'ict_visits Admin'
admin.site.site_title = 'ict_visits Admin Portal'
admin.site.index_title = 'Welcome to the ict_visits Admin Portal'