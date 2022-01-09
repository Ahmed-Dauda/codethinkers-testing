from django.urls import path

from . import views

from sms.views import(
    Categorieslistview,
     Courseslistview,
      Topicslistview,
      Topicsdetailview,
      Feedbackformview,
      Commentlistview,
      Commentlistviewsuccess,
    # UserProfilelistview,
      UserProfileForm,
      UserProfileUpdateForm,
      Admin_Result,
      Admin_result_detail_view,
      
) 

app_name = 'sms'

urlpatterns = [
  
    path('', Categorieslistview.as_view(), name='categorieslist'),
    path('courseslist/<pk>/', Courseslistview.as_view(), name='courseslist'),
    path('topicslistview/<pk>/', Topicslistview.as_view(), name='topicslistview'),
    path('topicsdetailview/<pk>/', Topicsdetailview.as_view(), name='topicsdetailview'),
    # path('signupview', signupview.as_view(), name ='signupview'),
    path('feedbackformview', Feedbackformview.as_view(), name ='feedbackformview'),
    path('admin_result', Admin_Result.as_view(), name ='admin_result'),
    path('commentlistview', Commentlistview.as_view(), name ='commentlistview'),
    path('commentlistviewsuccess', Commentlistviewsuccess.as_view(), name ='commentlistviewsuccess'),
    # path('userprofilelistview', UserProfilelistview.as_view(), name ='userprofilelistview'),
    path('userprofilelistview/<pk>/', views.check_marks_view, name ='userprofilelistview'),
    path('admin_result_detail_view/<pk>/', Admin_result_detail_view.as_view(), name ='admin_result_detail_view'),
    path('userprofileform', UserProfileForm.as_view(), name ='userprofileform'),
    path('userprofileupdateform/<pk>/', UserProfileUpdateForm.as_view(), name ='userprofileupdateform'),

 
]




