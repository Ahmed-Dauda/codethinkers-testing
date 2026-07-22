from django import forms
from .models import Student

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['full_name', 'admission_number', 'class_name', 'gender', 'date_of_birth', 'parent_phone']