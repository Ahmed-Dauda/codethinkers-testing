from django.urls import path

from . import views

app_name = 'student'

urlpatterns = [
    path('take-exam', views.take_exams_view,name='take-exam'),
    path('start-exam/<pk>/', views.start_exams_view,name='start-exam'),
    path('calculate_marks', views.calculate_marks_view,name='calculate_marks'),
    path('view_result', views.view_result_view,name='view_result'),
    path('check_marks/<pk>/', views.check_marks_view,name='check_marks'),
   
]




