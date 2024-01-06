from . import views
from django.urls import path
from .views import ReferralSignupView
from .views import become_referrer
        
app_name = 'users'

urlpatterns = [
    path('referral-signup/<str:referrer_code>/', ReferralSignupView.as_view(), name='referral_signup'),
    path('become-referrer/', become_referrer, name='become_referrer'),
 
   
]




