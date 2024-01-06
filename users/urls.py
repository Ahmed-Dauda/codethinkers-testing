from . import views
from django.urls import path
from .views import ReferralSignupView

        
app_name = 'users'

urlpatterns = [
    path('referral-signup/<str:referrer_code>/', ReferralSignupView.as_view(), name='referral_signup'),
# path('referral-signup/<str:referrer_code>/', referral_signup, name='referral_signup'),
 
   
]




