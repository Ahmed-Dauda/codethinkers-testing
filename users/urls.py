from . import views
from django.urls import path
from .views import ReferralSignupView, SchoolStudentView, SchoolSignupView, visit_stats_api
from .views import become_referrer

       
app_name = 'users'

urlpatterns = [
    path('visit-stats/', visit_stats_api, name='visit_stats_api'),
    path('api/online-users/', views.online_users_api, name='online_users_api'),

    path('dashboard/', views.dashboard_view, name='quick_dashboard'),
    path('school-signupp/', SchoolSignupView.as_view(), name='school_signup'),
    path('schoolstudentview/', SchoolStudentView, name='schoolstudentview'),
    path('referral-signup/<str:referrer_code>/', ReferralSignupView.as_view(), name='referral_signup'),
    path('become-referrer/', become_referrer, name='become_referrer'),
 
]




