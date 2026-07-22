from django.urls import path
from . import views

app_name = 'pos_attendant_system'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]