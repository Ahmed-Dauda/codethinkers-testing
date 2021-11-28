from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django import forms
from django.db import models 
from django.forms import ModelForm
from django import forms
from django.db import models 
from sms.models import Comment
from users.models import NewUser, BaseUserManager

class signupform(UserCreationForm):
    """docstring for signupform"""
    # TODO: write code...
    
    first_name = models.CharField(max_length = 225)
    last_name = models.CharField(max_length = 225)
    # email = models.EmailField(max_length = 225)
    
    
    class Meta:
        model = NewUser
        fields = [
            'first_name',
            'last_name',
            'country',
            'email',
            'password1',
            'password2'
            ]
            

from allauth.account.forms import SignupForm
from django import forms
from .models import *

class SimpleSignupForm(SignupForm):
    user_name = forms.CharField(max_length= 225, label='username')
    phone = forms.CharField(max_length=12, label='phone')
    country = forms.CharField(max_length=225, label='country')
    
    def save(self, request):
        user = super(SimpleSignupForm, self).save(request)
        user.phone = self.cleaned_data['phone']
        # user.user_name  = self.cleaned_data['user_name ']
        user.save()
        return user

# from sms.models import smsform

class smspostform(ModelForm):
    class Meta:
        
        # model = smsform
        fields= '__all__'
    
class feedbackform(ModelForm):
    class Meta:
        
        model = Comment
        fields= '__all__'