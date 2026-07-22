from django import forms
from .models import Student, Class, Teacher

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'class_enrolled']

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'teacher']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email']