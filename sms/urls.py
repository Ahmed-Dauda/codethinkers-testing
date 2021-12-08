from django.urls import path

from . import views
from sms.views import(
    Categorieslistview,
     Courseslistview,
      Topicslistview,
      Topicsdetailview,
    #   signupview,
    #   logout_view,
      Feedbackformview,
    #   Signupsuccess,
      Commentlistview,
      Commentlistviewsuccess,
      UserProfilelistview,
      UserProfileForm,
      UserProfileUpdateForm,
      
) 

app_name = 'sms'

urlpatterns = [
  
    path('', Categorieslistview.as_view(), name='categorieslist'),
    path('courseslist/<pk>/', Courseslistview.as_view(), name='courseslist'),
    path('topicslistview/<pk>/', Topicslistview.as_view(), name='topicslistview'),
    path('topicsdetailview/<pk>/', Topicsdetailview.as_view(), name='topicsdetailview'),
    # path('signupview', signupview.as_view(), name ='signupview'),
    path('feedbackformview', Feedbackformview.as_view(), name ='feedbackformview'),
    # path('signupsuccess', Signupsuccess.as_view(), name ='signupsuccess'),
    path('commentlistview', Commentlistview.as_view(), name ='commentlistview'),
    path('commentlistviewsuccess', Commentlistviewsuccess.as_view(), name ='commentlistviewsuccess'),
    path('userprofilelistview', UserProfilelistview.as_view(), name ='userprofilelistview'),
    path('userprofileform', UserProfileForm.as_view(), name ='userprofileform'),
    path('userprofileupdateform/<pk>/', UserProfileUpdateForm.as_view(), name ='userprofileupdateform'),
    # path('logout',views.logout_view , name ='logout'),
    # path('notification',views.notification , name ='notification'),
    # path("password_reset", views.password_reset_request, name="password_reset")
   
]




