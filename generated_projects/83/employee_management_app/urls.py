from django.urls import path
from . import views

app_name = 'employee_management'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('employees/', views.EmployeeListView.as_view(), name='employee_list'),
    path('employees/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('employees/create/', views.EmployeeCreateView.as_view(), name='employee_create'),
    path('employees/<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee_update'),
    path('employees/<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='employee_delete'),
    path('employees/<int:pk>/checkin/', views.CheckInView.as_view(), name='employee_checkin'),
    path('employees/<int:pk>/checkout/', views.CheckOutView.as_view(), name='employee_checkout'),
]