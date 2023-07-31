from django.urls import path

from . import views


        
app_name = 'student'

urlpatterns = [

    

      
    path('verify/<str:id>/', views.verify,name='verify'),
    # path('student/verify/<str:id>/', views.verify_payment, name='verify_payment'),
  
    path('process', views.process,name='process'),
    # new url
    path('take-exam', views.take_exams_view,name='take-exam'),
    path('start-exam/<pk>/', views.start_exams_view,name='start-exam'),
    path('calculate_marks', views.calculate_marks_view,name='calculate_marks'),
    path('view_result', views.view_result_view,name='view_result'),
    # selling pdf segment
    path('upload_pdf/', views.upload_pdf_document, name='upload_pdf_document'),
    path('pdf_document_list/', views.pdf_document_list, name='pdf_document_list'),
    # path('pdf_document_detail/<int:document_id>/', views.pdf_document_detail, name='pdf_document_detail'),
    # end
    path('pdf/<pk>/', views.pdf_id_view,name='pdf'),
    # path('check_marks/<pk>/', views.check_marks_view,name='check_marks'),
    path('verify/', views.verify_cert, name='verify_cert'),

    path('verify/<str:certificate_code>/', views.verify_certificate, name='verify_certificate'),
    
   
]




