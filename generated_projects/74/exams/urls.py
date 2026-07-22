from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    path('', views.home, name='home'),
]