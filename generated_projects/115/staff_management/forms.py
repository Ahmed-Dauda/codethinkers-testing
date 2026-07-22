from django import forms
from .models import Employee, Department

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'department']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']