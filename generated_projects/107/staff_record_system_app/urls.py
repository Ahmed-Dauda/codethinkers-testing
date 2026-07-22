from django.urls import path
from . import views

app_name = 'staff_record_system_app'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('staff/', views.StaffListView.as_view(), name='staff_list'),
    path('staff/<int:pk>/', views.StaffDetailView.as_view(), name='staff_detail'),
    path('departments/', views.DepartmentListView.as_view(), name='department_list'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department_detail'),
]