from django.urls import path
from teacher import views
from django.contrib.auth.views import LoginView

app_name = 'teacher'

urlpatterns = [
path('student-dashboard', views.student_dashboard_view,name='student-dashboard'),
path('teacherclick', views.teacherclick_view),
path('teacherlogin', LoginView.as_view(template_name='teacher/teacherlogin.html'),name='teacherlogin'),
path('teachersignup', views.teacher_signup_view,name='teachersignup'),
path('teacher-dashboard', views.teacher_dashboard_view,name='teacher-dashboard'),

]