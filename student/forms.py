
from django.forms import ModelForm
from student.models import Payment

from django import forms
from .models import Payment

from django import forms
from .models import PDFDocument




class PDFDocumentForm(forms.ModelForm):
    class Meta:
        model = PDFDocument
        fields = ['title', 'desc','price' ,'pdf_file']




