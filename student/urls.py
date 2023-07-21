from django.urls import path

from . import views

from student.views import course_list, add_to_cart, cart, update_cart, checkout, order_confirmation

        
app_name = 'student'

urlpatterns = [
    # add to cart 
    path('courses/', course_list, name='course_list'),
    path('course/<int:course_id>/add-to-cart/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('cart/<int:cart_item_id>/update/', update_cart, name='update_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order/<int:order_id>/confirmation/', order_confirmation, name='order_confirmation'),
    # end
    

      
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




