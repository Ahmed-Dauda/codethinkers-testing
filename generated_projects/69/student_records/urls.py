from django.urls import path
from . import views

app_name = 'student_records'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register_student, name='register_student'),
    path('dashboard/', views.dashboard, name='dashboard'),
]