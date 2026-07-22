from django.urls import path
from . import views

app_name = 'school_management'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('students/create/', views.StudentCreateView.as_view(), name='student_create'),
    path('students/update/<int:pk>/', views.StudentUpdateView.as_view(), name='student_update'),
    path('teachers/', views.TeacherListView.as_view(), name='teacher_list'),
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('shoprecords/', views.DailyShopRecordListView.as_view(), name='shoprecord_list'),
    path('shoprecords/<int:pk>/', views.DailyShopRecordDetailView.as_view(), name='shoprecord_detail'),
    path('shoprecords/create/', views.DailyShopRecordCreateView.as_view(), name='shoprecord_create'),
    path('violations/', views.LightViolationListView.as_view(), name='violation_list'),
    path('violations/create/', views.LightViolationCreateView.as_view(), name='violation_create'),
    path('violations/<int:pk>/', views.LightViolationDetailView.as_view(), name='violation_detail'),
]