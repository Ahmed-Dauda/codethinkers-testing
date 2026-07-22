from django import forms
from .models import Student, Attendance, Grade

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status']

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'score']