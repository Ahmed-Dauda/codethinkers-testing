from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email, user_username
from django.shortcuts import redirect
from smtplib import SMTPException
from django.urls import reverse

import logging
logger = logging.getLogger(__name__)

class CustomAccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        # Skip only during signup
        if signup:
            return
        return super().send_confirmation_mail(request, emailconfirmation, signup)


# class CustomAccountAdapter(DefaultAccountAdapter):

#     def send_confirmation_mail(self, request, emailconfirmation, signup):
#         try:
#             super().send_confirmation_mail(request, emailconfirmation, signup)
#         except SMTPException as e:
#             print(f"Email confirmation failed: {e}")
#             # You can log this or alert admins
