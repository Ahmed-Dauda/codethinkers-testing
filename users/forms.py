from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django import forms
from django.db import models 
from django.forms import ModelForm
from django import forms
from django.db import models 
from sms.models import Comment
from allauth.account.forms import SignupForm
from django import forms
from .models import *
from users.models import NewUser

# models.py

from django.db import models

# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
# from .models import ReferrerProfile




country_choice = [
    ('select country here', 'select country here'),('Nigeria', 'Nigeria'), ('United State', 'United State'), ('Afghanistan', 'Afghanistan'),
    ('Albania', 'Albania'),('Algeria', 'Algeria'), ('Andorra', 'Andorra'), ('Angola', 'Angola'),
    ('Antigua and Barbuda', 'Antigua and Barbuda'),('Argentina', 'Argentina'), ('Armenia', 'Armenia'), ('Australia', 'Australia'),
    ('Austria', 'Austria'),('Azerbaijan', 'Azerbaijan'), ('Bahamas', 'Bahamas'), ('	Bahrain', '	Bahrain'),
    ('Bahamas', 'Bahamas'),('Bahrain', 'Bahrain'), ('Bangladesh', 'Bangladesh'), ('Barbados', 'Barbados'),
    ('Belarus', 'Belarus'),('Belgium', 'Belgium'), ('Belize', 'Belize'), ('Benin', 'Benin'),
    ('Bhutan', 'Bhutan'),('Bolivia', 'Bolivia'), ('Bosnia and Herzegovina', 'Bosnia and Herzegovina'), ('Botswana', 'Botswana'),
    ('Brazil', 'Brazil'),('Brunei', 'Brunei'), ('Bulgaria', 'Bulgaria'), ('Burkina Faso', 'Burkina Faso'),
    ('Burundi', 'Burundi'),('Côte d"Ivoire', 'Côte d"Ivoire'), ('Cabo Verde', '	Cabo Verde'), ('Cambodia', 'Cambodia'),
    ('Cameroon', 'Cameroon'),('Canada', 'Canada'), ('Central African Republic', 'Central African Republic'), ('Chad', 'Chad'),
    ('Chile', 'Chile'),('China', 'China'), ('Colombia', 'Colombia'), ('Comoros', 'Comoros'), ('Congo ','Congo'),
    ('Costa Rica', 'Costa Rica'),('Croatia', 'Croatia'), ('Cuba', 'Cuba'), ('Cyprus', 'Cyprus'),('Dominican Republic','Dominican Republic'),
    ('Czechia ', 'Czechia'),('Denmark', 'Denmark'), ('Djibouti', 'Djibouti'), ('Dominica', 'Dominica'),

]


from django import forms
from allauth.account.forms import SignupForm

class SimpleSignupForm(SignupForm):
    first_name = forms.CharField(max_length=12, label='First-name')
    last_name = forms.CharField(max_length=225, label='Last-name')
    # referral_code = forms.CharField(max_length=20, required=False, label='Referral Code')
    phone_number = forms.CharField(max_length=225, widget=forms.HiddenInput(), required=False)
    # phone_number = forms.CharField(max_length=225, label='Referral Code', widget=forms.TextInput(attrs={'placeholder': 'if available'}),required=False)
    countries = forms.ChoiceField(choices=country_choice, label='Country')
    
    def save(self, request):
        user = super(SimpleSignupForm, self).save(request)
        user.phone_number = self.cleaned_data.get('phone_number', '')  # Use get() to handle the case when phone_number is not provided.
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.countries = self.cleaned_data['countries']
        # user.referral_code  = self.cleaned_data['referral_code']
        
        user.save()
        
        return user


# users/forms.py
from django import forms
from student.models import ReferrerMentor
from django.contrib.auth import get_user_model


class ReferrerMentorForm(forms.ModelForm):
    class Meta:
        model = ReferrerMentor
        fields = ['name', 'courses', 'phone_no']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude the 'referrer' field from the form
        if 'referrer' in self.fields:
            self.fields['referrer'].widget = forms.HiddenInput()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.referrer_code = self.cleaned_data.get('referrer_code', '')
        if commit:
            instance.save()
        return instance




# from allauth.account.forms import SignupForm
# from django import forms

# class SimpleSignupForm(SignupForm):
#     first_name = forms.CharField(max_length=12, label='First-name')
#     last_name = forms.CharField(max_length=225, label='Last-name')
#     # phone_number = forms.CharField(max_length=225, widget=forms.HiddenInput(), required=False)
#     phone_number = forms.CharField(max_length=225, label='Referral Code', widget=forms.TextInput(attrs={'placeholder': 'if available'}), required=False)
#     countries = forms.ChoiceField(choices=country_choice, label='Country')
#     # referral_code = forms.CharField(max_length=20, widget=forms.HiddenInput(), required=False)
    
#     def save(self, request):
#         user = super(SimpleSignupForm, self).save(request)
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.countries = self.cleaned_data['countries']
        
#         # Retrieve the referral code from the form data
#         referral_code = self.cleaned_data.get('phone_number', '')
        
#         # If a referral code is provided, you can handle it here
#         if referral_code:
#             # Perform actions with the referral code, e.g., associate it with the user
#             # user.referral_code = referral_code
            
#             pass
        
#         user.save()
        
#         return user




# forms.py
# from allauth.account.forms import SignupForm
# from django import forms
# from .models import ReferrerProfile  # Assuming you've created a ReferrerProfile model

# class ReferrerSignupForm(SignupForm):
#     first_name = forms.CharField(max_length=12, label='First-name')
#     last_name = forms.CharField(max_length=225, label='Last-name')
#     countries = forms.ChoiceField(choices=country_choice, label='Country')
#     referral_code = forms.CharField(max_length=20, required=False, label='Referral Code')

#     def save(self, request):
#         user = super(ReferrerSignupForm, self).save(request)
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.countries = self.cleaned_data['countries']
#         user.save()

#         # Process referral code and associate referrer
#         referral_code = self.cleaned_data.get('referral_code')
#         if referral_code:
#             try:
#                 referrer = ReferrerProfile.objects.get(referral_code=referral_code).user
#                 user_profile, created = ReferrerProfile.objects.get_or_create(user=user)
#                 user_profile.referrer = referrer
#                 user_profile.save()
#             except ReferrerProfile.DoesNotExist:
#                 pass

#         return user
 


# from sms.models import smsform

class smspostform(ModelForm):
    class Meta:
        
        # model = smsform
        fields= '__all__'
    
class feedbackform(ModelForm):
    class Meta:
        
        model = Comment
        fields= '__all__'

class userprofileform(ModelForm):
    class Meta:
        
        # model = Profile
        fields= '__all__'