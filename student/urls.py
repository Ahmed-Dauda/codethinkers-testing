from django.urls import path

from sms.views import update_referrer_mentor

from . import views


        
app_name = 'student'

urlpatterns = [

    path('verify/<str:code>/', views.verify_certificate, name='verify_certificate'),
    path('certificate/pdf/<int:pk>/', views.pdf_id_view, name='pdf_id_view'),
    path('paystack/webhook/', views.paystack_webhook, name='paystack_webhook'),
    path('referrer_mentor_detail/<int:pk>/', update_referrer_mentor, name='referrer_mentor_detail'),
    path('take-exam', views.take_exams_view,name='take-exam'),
    path('start-exam/<pk>/', views.start_exams_view,name='start-exam'),
    path('calculate_marks', views.calculate_marks_view,name='calculate_marks'),
    path('view_result', views.view_result_view,name='view_result'),
    path('pdf_document_list/', views.pdf_document_list, name='pdf_document_list'),

]




