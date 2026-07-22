from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/update/<int:pk>/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
]