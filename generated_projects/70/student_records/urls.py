from django.urls import path
from . import views

app_name = 'student_records'

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.student_list, name='student_list'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register_student, name='register_student'),
]