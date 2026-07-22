from django import forms
from .models import Enrollment, Progress

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course']

class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['completed', 'grade']