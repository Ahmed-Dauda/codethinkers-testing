# editor/forms.py
from django import forms
from .models import File

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'image']  # content not needed for images
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
