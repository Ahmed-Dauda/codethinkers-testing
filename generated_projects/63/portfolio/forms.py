from django import forms
from django.core.mail import send_mail

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        send_mail(
            f"Contact from {self.cleaned_data['name']}",
            self.cleaned_data['message'],
            self.cleaned_data['email'],
            ['your_email@example.com'],
        )