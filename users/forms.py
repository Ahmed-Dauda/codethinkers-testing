from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django import forms
from django.db import models 
from django.forms import ModelForm
from student.models import ReferrerMentor
from django.contrib.auth import get_user_model
from sms.models import Comment
from allauth.account.forms import SignupForm
from .models import *
from users.models import NewUser

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

from quiz.models import School

# class SchoolStudentForm(SignupForm):
#     first_name = forms.CharField(max_length=12, label='First Name 1')
#     last_name = forms.CharField(max_length=50, label='Last Name')
#     referral_code = forms.CharField(max_length=20, required=False, label='Referral Code')
#     phone_number = forms.CharField(max_length=225, widget=forms.HiddenInput(), required=False)
#     countries = forms.ChoiceField(choices=country_choice, label='Country')
#     school = forms.CharField(max_length=100, label='School')  # Add the school field
    
#     def save(self, request):
#         user = super(SchoolStudentForm, self).save(request)
#         user.phone_number = self.cleaned_data.get('phone_number', '')
#         user.first_name = self.cleaned_data['first_name 1']
#         user.last_name = self.cleaned_data['last_name']
#         user.countries = self.cleaned_data['countries']
#         user.referral_code = self.cleaned_data.get('referral_code', '')
#         user.school = self.cleaned_data.get('school', '')  # Handle the school field
        
#         user.save()
        
#         return user
    
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

# class SimpleSignupForm(SignupForm):
#     first_name = forms.CharField(max_length=12, label='First-name')
#     last_name = forms.CharField(max_length=225, label='Last-name')
#     phone_number = forms.CharField(max_length=225, widget=forms.HiddenInput(), required=False)
#     countries = forms.ChoiceField(choices=country_choice, label='Country')

#     honeypot = forms.CharField(required=False, widget=forms.HiddenInput())  # 🐝 HTML honeypot
#     js_honeypot = forms.CharField(required=False, widget=forms.HiddenInput())  # 🛡️ JavaScript honeypot

#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop('request', None)
#         super().__init__(*args, **kwargs)

#     def clean(self):
#         cleaned_data = super().clean()

#         # 🐝 HTML Honeypot trap
#         if cleaned_data.get('honeypot'):
#             raise ValidationError("Something went wrong. Please try again.")

#         # 🛡️ JavaScript Honeypot
#         js_trap = cleaned_data.get('js_honeypot')
#         if js_trap != 'human':
#             raise ValidationError("Something went wrong. Please try again.")

#         # 🕒 Time-based Bot Detection
#         if self.request:
#             form_created_at = self.request.session.get('form_created_at')
#             if form_created_at:
#                 try:
#                     from datetime import datetime
#                     elapsed = timezone.now() - datetime.fromisoformat(form_created_at)
#                     if elapsed < timedelta(seconds=5):
#                         raise ValidationError("Something went wrong. Please try again.")
#                 except Exception:
#                     pass  # Ignore time parse failures

#         return cleaned_data

#     def save(self, request):
#         user = super(SimpleSignupForm, self).save(request)
#         user.phone_number = self.cleaned_data.get('phone_number', '')
#         user.first_name = self.cleaned_data.get('first_name', '')
#         user.last_name = self.cleaned_data.get('last_name', '')
#         user.countries = self.cleaned_data.get('countries', '')
#         user.save()
#         return user


# class SimpleSignupForm(SignupForm):
#     first_name = forms.CharField(max_length=12, label='First-name')
#     last_name = forms.CharField(max_length=225, label='Last-name')
#     phone_number = forms.CharField(max_length=225, widget=forms.HiddenInput(), required=False)
#     countries = forms.ChoiceField(choices=country_choice, label='Country')

#     honeypot = forms.CharField(required=False, widget=forms.HiddenInput())  # Fake field

#     def clean(self):
#         cleaned_data = super().clean()

#         # 🐝 Honeypot
#         if cleaned_data.get('honeypot'):
#             raise ValidationError("Bot detected.")

#         # 🕒 Time-based detection
#         request = self.request
#         form_created_at = request.session.get('form_created_at')
#         if form_created_at:
#             try:
#                 elapsed = timezone.now() - timezone.datetime.fromisoformat(form_created_at)
#                 if elapsed < timedelta(seconds=5):
#                     raise ValidationError("Network issue detected")
#             except Exception:
#                 pass  # fallback to ignoring error silently

#         return cleaned_data

#     def save(self, request):
#         user = super().save(request)
#         user.phone_number = self.cleaned_data.get('phone_number', '')
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.countries = self.cleaned_data['countries']
#         user.save()
#         return user


# original form without honeypot

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



class SchoolStudentSignupForm(SignupForm):
    first_name = forms.CharField(max_length=222, label='First-name')
    last_name = forms.CharField(max_length=225, label='Last-name')
    phone_number = forms.CharField(max_length=225, widget=forms.HiddenInput(), required=False)
    admission_no = forms.CharField(max_length=50, label='Aadmission Number')
    student_class = forms.CharField(label='Student Class', )
    countries = forms.ChoiceField(choices=country_choice, label='Country')
    school = forms.ModelChoiceField(queryset=School.objects.all(), label='School', required=True)
   
    def save(self, request):
        user = super(SchoolStudentSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data.get('phone_number', '')
        user.admission_no = self.cleaned_data['admission_no']
        user.student_class = self.cleaned_data['student_class']
        user.countries = self.cleaned_data['countries']
        user.school = self.cleaned_data['school']
        
        user.save()
        
        return user



class SchoolSignupForm(forms.ModelForm):
    class Meta:
        model = School
        fields = "__all__"

    def clean_logo(self):
        logo = self.cleaned_data.get('logo')

        # Perform additional validation for the logo field if needed
        # For example, check if the file is an image, meets certain size requirements, etc.

        return logo

    def clean_principal_signature(self):
        principal_signature = self.cleaned_data.get('principal_signature')

        # Perform additional validation for the principal_signature field if needed

        return principal_signature


from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


class ReferrerMentorForm(forms.ModelForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput())  # HTML bot trap
    js_honeypot = forms.CharField(required=False, widget=forms.HiddenInput())  # JS bot trap

    class Meta:
        model = ReferrerMentor
        fields = ['name', 'phone_no']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # capture request
        super().__init__(*args, **kwargs)
        # Hide the 'referrer' field
        if 'referrer' in self.fields:
            self.fields['referrer'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()

        # 🐝 Honeypot trap
        if cleaned_data.get('honeypot'):
            raise ValidationError("Something went wrong. Please try again.")

        # 🛡️ JavaScript bot trap
        if cleaned_data.get('js_honeypot') != 'human':
            raise ValidationError("Something went wrong. Please try again.")

        # ⏱️ Time-based detection
        if self.request:
            form_created_at = self.request.session.get('form_created_at')
            if form_created_at:
                try:
                    elapsed = timezone.now() - timezone.datetime.fromisoformat(form_created_at)
                    if elapsed < timedelta(seconds=5):
                        raise ValidationError("Something went wrong. Please try again.")
                except Exception:
                    pass  # Ignore parse errors

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.referrer_code = self.cleaned_data.get('referrer_code', '')
        if commit:
            instance.save()
        return instance
class ReferrerMentorForm(forms.ModelForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput())  # Bot trap 1
    js_honeypot = forms.CharField(required=False, widget=forms.HiddenInput())  # Bot trap 2

    class Meta:
        model = ReferrerMentor
        fields = ['name', 'phone_no']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if 'referrer' in self.fields:
            self.fields['referrer'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('honeypot'):
            raise ValidationError("Something went wrong. Please try again.")

        if cleaned_data.get('js_honeypot') != 'human':
            raise ValidationError("Something went wrong. Please try again.")

        if self.request:
            created_at = self.request.session.get('referrer_form_created_at')
            if created_at:
                try:
                    elapsed = timezone.now() - timezone.datetime.fromisoformat(created_at)
                    if elapsed < timedelta(seconds=5):
                        raise ValidationError("Form submitted too quickly. Please try again.")
                except Exception:
                    pass

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.referrer_code = self.cleaned_data.get('referrer_code', '')
        if commit:
            instance.save()
        return instance

# working before
# class ReferrerMentorForm(forms.ModelForm):
#     class Meta:
#         model = ReferrerMentor
#         fields = ['name', 'phone_no']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Hide the 'referrer' field
#         if 'referrer' in self.fields:
#             self.fields['referrer'].widget = forms.HiddenInput()

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         instance.referrer_code = self.cleaned_data.get('referrer_code', '')
#         if commit:
#             instance.save()
#         return instance


# class ReferrerMentorForm(forms.ModelForm):
#     class Meta:
#         model = ReferrerMentor
#         fields = ['name', 'phone_no']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Exclude the 'referrer' field from the form
#         if 'referrer' in self.fields:
#             self.fields['referrer'].widget = forms.HiddenInput()

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         instance.referrer_code = self.cleaned_data.get('referrer_code', '')
#         if commit:
#             instance.save()
#         return instance




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