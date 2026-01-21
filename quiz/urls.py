from django.urls import path

from . import views

     
app_name = 'quiz'

urlpatterns = [
    path('ai-topics-generator-obj/', views.ai_topics_generator_obj, name='ai_topics_generator_obj'),

    path('ai-topics-generator/', views.ai_topics_generator, name='ai_topics_generator'),

    path('ai-assessment-selector/', views.ai_assessment_selector, name='ai_assessment_selector'),
    path('ai-summative-assessment/', views.ai_summative_assessment, name='ai_summative_assessment'),
    path('ai-question-generator/', views.generate_ai_questions, name='generate_ai_questions'),
    
    path('take-exam', views.take_exams_view,name='take-exam'),
    path('start-exam/<int:pk>/', views.start_exams_view, name='start-exam'),
    path('calculate_marks_assessment/', views.calculate_marks_assessment, name='calculate_marks_assessment'),
    path('view_result', views.view_result_view,name='view_result'),
    # path('register-student/', views.register_student, name='register_student'),
    # path('school-dashboard/<pk>/', views.school_dashboard, name='school_dashboard'),
   
]




