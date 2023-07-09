from django.urls import path

from . import views
# from .views import verify_payment
from django.urls import path


app_name = 'student'

urlpatterns = [
    path('payment-status/<str:reference>/', views.get_payment_status, name='payment-status'),
    path('customer-references/', views.customer_references_view, name='customer_references'),
    path('process_payment', views.process_payment, name='process_payment'),
    path('webhook/', views.handle_webhook, name='webhook'),
 
    # path('initiate-payment', views.initiate_payment,name='initiate-payment'),
    # path('<str:ref>/', views.verify_payment,name='verify-payment'),
    # path('verify-payment/', views.verify_payment, name='verify-payment'),
    path('customer_references_view', views.customer_references_view,name='customer_references_view'),
    # path('success', views.succes,name='success'),
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




