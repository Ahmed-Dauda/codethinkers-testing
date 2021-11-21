from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.db import models 
from django.forms import ModelForm
from django import forms
from django.db import models 
from sms.models import Comments
from django.contrib.auth import get_user_model
User = get_user_model()

class signupform(UserCreationForm):
    """docstring for signupform"""
    # TODO: write code...
    
    first_name = models.CharField(max_length = 225)
    last_name = models.CharField(max_length = 225)
    # email = models.EmailField(max_length = 225)
    
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'country',
            'email',
            'password1',
            'password2'
            ]
            


# from sms.models import smsform

class smspostform(ModelForm):
    class Meta:
        
        # model = smsform
        fields= '__all__'
    
class feedbackform(ModelForm):
    class Meta:
        
        model = Comments
        fields= '__all__'