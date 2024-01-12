
from django import forms
from .models import School

# class StudentRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ['name', 'admission_no', 'date_of_birth', 'address', 'school']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Add a dropdown list for the 'school' field
#         self.fields['school'].queryset = School.objects.all()
#         self.fields['school'].empty_label = 'Select a school'

#     def save(self, commit=True):
#         student = super().save(commit=False)
#         # You can perform any additional actions before saving, if needed
#         if commit:
#             student.save()
#         return student
