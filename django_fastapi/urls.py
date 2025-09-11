from django.urls import path
from . import views

urlpatterns = [
    path('frontend/', views.frontend, name='frontend'),
    
]
