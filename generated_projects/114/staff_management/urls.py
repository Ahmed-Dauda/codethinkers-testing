from django.urls import path
from . import views

app_name = 'staff_management'

urlpatterns = [
    path('staff/', views.StaffListView.as_view(), name='staff_list'),
    path('staff/<int:pk>/', views.StaffDetailView.as_view(), name='staff_detail'),
    path('attendance/', views.AttendanceListView.as_view(), name='attendance_list'),
    path('attendance/<int:pk>/', views.AttendanceDetailView.as_view(), name='attendance_detail'),
    path('performance-reviews/', views.PerformanceReviewListView.as_view(), name='performance_review_list'),
    path('performance-reviews/<int:pk>/', views.PerformanceReviewDetailView.as_view(), name='performance_review_detail'),
    path('performancereview/', views.PerformanceReviewListView.as_view(), name='performancereview_list'),
    path('performancereview/<int:pk>/', views.PerformanceReviewDetailView.as_view(), name='performancereview_detail'),
]