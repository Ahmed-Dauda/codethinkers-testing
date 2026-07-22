from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('enroll/', views.EnrollmentCreateView.as_view(), name='enrollment_create'),
    path('progress/<int:pk>/update/', views.ProgressUpdateView.as_view(), name='progress_update'),
    path('enrollment/create/', views.EnrollmentCreateView.as_view(), name='enrollment_create'),
    path('progress/<int:pk>/update/', views.ProgressUpdateView.as_view(), name='progress_update'),
]