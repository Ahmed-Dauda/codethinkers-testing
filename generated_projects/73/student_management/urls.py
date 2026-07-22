from django.urls import path
from . import views

app_name = 'student_management'

urlpatterns = [
    path('', views.home, name='home'),
]