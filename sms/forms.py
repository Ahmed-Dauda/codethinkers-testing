# from tkinter import Widget
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django import forms
from django.db import models 
from django.forms import ModelForm
from django import forms
from django.db import models 
from sms.models import Comment, Blogcomment
from users.models import NewUser, BaseUserManager
from tinymce.widgets import TinyMCE
class smspostform(ModelForm):
    class Meta:
        
        # model = smsform
        fields= '__all__'
    
class feedbackform(ModelForm):
    class Meta:
        
        model = Comment
        fields= '__all__'
        

class BlogcommentForm(forms.ModelForm):
    content =forms.CharField(widget=TinyMCE(attrs={'cols': 50, 'rows': 30}))
    class Meta:
        model = Blogcomment
        fields = ('name','content',)
        
       
       