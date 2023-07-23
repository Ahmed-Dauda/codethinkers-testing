from django.urls import path

from . import views


        
app_name = 'student'

urlpatterns = [

    

      
    path('verify/<str:id>/', views.verify,name='verify'),
    # path('verify-payment/', views.verify_payment, name='verify-payment'),
  
    path('process', views.process,name='process'),
    # new url
    path('take-exam', views.take_exams_view,name='take-exam'),
    path('start-exam/<pk>/', views.start_exams_view,name='start-exam'),
    path('calculate_marks', views.calculate_marks_view,name='calculate_marks'),
    path('view_result', views.view_result_view,name='view_result'),
    
    path('pdf/<pk>/', views.pdf_id_view,name='pdf'),
    # path('check_marks/<pk>/', views.check_marks_view,name='check_marks'),
    path('verify/', views.verify_cert, name='verify_cert'),

    path('verify/<str:certificate_code>/', views.verify_certificate, name='verify_certificate'),
    
   
]




