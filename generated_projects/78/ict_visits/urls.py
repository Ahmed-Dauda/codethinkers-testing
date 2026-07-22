from django.urls import path
from . import views

app_name = 'ict_visits'

urlpatterns = [
    path('', views.home, name='home'),
    path('export/csv/', views.export_to_csv, name='export_to_csv'),
]