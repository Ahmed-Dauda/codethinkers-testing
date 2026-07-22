from django.contrib import admin
from .models import Employee, Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'department', 'check_in_time', 'check_out_time', 'created_at', 'updated_at')
    search_fields = ('name', 'email')
    list_filter = ('department',)