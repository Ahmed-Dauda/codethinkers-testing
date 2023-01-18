from django.urls import path
from . import views

from sms.views import(
    Categorieslistview,
     
     Topicslistview,
    #   Topic_list,
    
    # dashboard url
       Category,
       Table,
       Homepage,
       AlertView,
       Courseslistview,

    #    end
    
      Courseslistdescview,
      Topicsdetailview,
      Feedbackformview,
      Commentlistview,
      Commentlistviewsuccess,
      UserProfilelistview,
      UserProfileForm,
      Certificates,
      UserProfileUpdateForm,
      Admin_result,
      Admin_detail_view,
      Bloglistview,
      Blogdetaillistview,
      Baseblogview,
      BlogcommentCreateView,
    #   display_latestnews,
      
) 

app_name = 'sms'

urlpatterns = [
  
    # path('', Categorieslistview.as_view(), name='categorieslist'),
    
    # new dashboard urls
    path('home', Category.as_view(), name='home'),
    path('table', Table.as_view(), name='table'),
    path('', Homepage.as_view(), name='homepage'),
    path('alert', AlertView.as_view(), name='alert'),
    path('courseslist/<pk>/', Courseslistview.as_view(), name='courseslist'),
  
    # end
    
   
    path('courseslistdesc/<pk>/', Courseslistdescview.as_view(), name='courseslistdesc'),
    path('topicslistview/<pk>/', Topicslistview.as_view(), name='topicslistview'),
    path('topicsdetailview/<slug:slug>/', Topicsdetailview.as_view(), name='topicsdetailview'),
    # path('signupview', signupview.as_view(), name ='signupview'),
    path('feedbackformview', Feedbackformview.as_view(), name ='feedbackformview'),
    path('commentlistview', Commentlistview.as_view(), name ='commentlistview'),
    path('commentlistviewsuccess', Commentlistviewsuccess.as_view(), name ='commentlistviewsuccess'),
    path('myprofile', UserProfilelistview.as_view(), name ='myprofile'),

    path('certificates/<pk>/', views.Certificates, name ='certificates'),
    # path('topic', views.Topic_list, name="topic"),

    path('admin_result', Admin_result.as_view(), name ='admin_result'),
    path('admin_result_detail_view/<pk>/', Admin_detail_view, name ='admin_result_detail_view'),
    path('userprofileform', UserProfileForm.as_view(), name ='userprofileform'),
    path('userprofileupdateform/<pk>/', UserProfileUpdateForm.as_view(), name ='userprofileupdateform'),
    path('bloglistview', Bloglistview.as_view(), name ='bloglistview'),
    path('blog/<slug:slug>/', Blogdetaillistview.as_view(), name='blogdetaillistview'),
    path('baseview/<pk>/',  Baseblogview.as_view(), name='baseview'),
    path('blog/<slug:slug>/blogcommentform/', BlogcommentCreateView.as_view(), name ='blogcommentform'),
    
    # new pagination url
    path("terms",views.KeywordListView.as_view(),name="terms"),
    path("terms/<int:page>",views.listing,name="terms-by-page"),
    path('terms.json/',views.listing_api, name='terms-api'),
    path("faux",views.AllKeywordsView.as_view(),name="faux"),
 
]

# urlpatterns = [
#     path(
#         "terms",
#         views.KeywordListView.as_view(),
#         name="terms"),
#       path(
#         "terms/<int:page>",
#         views.listing,
#         name="terms-by-page"
#     ),
#     path('terms.json/',views.listing_api, name='terms-api'),
# ]




