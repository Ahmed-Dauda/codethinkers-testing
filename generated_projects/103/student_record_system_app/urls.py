from django.urls import path
from .views import HomeView, StudentListView, StudentDetailView, AttendanceListView, AttendanceDetailView, GradeListView, GradeDetailView

app_name = 'student_record_system_app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('students/', StudentListView.as_view(), name='student_list'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('attendance/', AttendanceListView.as_view(), name='attendance_list'),
    path('attendance/<int:pk>/', AttendanceDetailView.as_view(), name='attendance_detail'),
    path('grades/', GradeListView.as_view(), name='grade_list'),
    path('grades/<int:pk>/', GradeDetailView.as_view(), name='grade_detail'),
]