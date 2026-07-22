from django.urls import path
from . import views

app_name = 'hospital'

urlpatterns = [
    path('', views.home, name='home'),
    path('patient/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patient/create/', views.patient_create, name='patient_create'),
    path('patient/update/<int:pk>/', views.patient_update, name='patient_update'),
]