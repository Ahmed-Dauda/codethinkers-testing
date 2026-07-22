from django import forms
from .models import ContactFormSubmission

class ContactFormSubmissionForm(forms.ModelForm):
    class Meta:
        model = ContactFormSubmission
        fields = ['name', 'email', 'message']