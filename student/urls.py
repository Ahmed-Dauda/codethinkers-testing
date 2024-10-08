from django.urls import path

from sms.views import update_referrer_mentor

from . import views


        
app_name = 'student'

urlpatterns = [

    path('verify/<str:code>/', views.verify_certificate, name='verify_certificate'),
    path('certificate/pdf/<int:pk>/', views.pdf_id_view, name='pdf_id_view'),
    
    path('paystack/webhook/', views.paystack_webhook, name='paystack_webhook'),
#   testing  path('pdf/<pk>/', views.pdf_id_view,name='pdf'),
    # path('withdrawal/', views.withdrawal_request, name='withdrawal_request'),
    # URL for updating a referrer mentor
    path('referrer_mentor_detail/<int:pk>/', update_referrer_mentor, name='referrer_mentor_detail'),
   
    # path('process', views.process,name='process'),
    # new url
    path('take-exam', views.take_exams_view,name='take-exam'),
    path('start-exam/<pk>/', views.start_exams_view,name='start-exam'),
    path('calculate_marks', views.calculate_marks_view,name='calculate_marks'),
    path('view_result', views.view_result_view,name='view_result'),

    # selling pdf segment
    # path('upload_pdf/', views.upload_pdf_document, name='upload_pdf_document'),
    path('pdf_document_list/', views.pdf_document_list, name='pdf_document_list'),
    # path('pdf_document_detail/<str:pk>/', views.pdf_document_detail, name='pdf_document_detail'),
    # end

    
    # path('check_marks/<pk>/', views.check_marks_view,name='check_marks'),
    # path('verify/', views.verify_cert, name='verify_cert'),
   
]




