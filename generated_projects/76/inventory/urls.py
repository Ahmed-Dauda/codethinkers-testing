from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('product/create/', views.product_create, name='product_create'),
]