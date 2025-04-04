from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email, user_username
from django.shortcuts import redirect
from smtplib import SMTPException

class CustomAccountAdapter(DefaultAccountAdapter):

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        try:
            super().send_confirmation_mail(request, emailconfirmation, signup)
        except SMTPException as e:
            print(f"Email confirmation failed: {e}")
            # You can log this or alert admins
