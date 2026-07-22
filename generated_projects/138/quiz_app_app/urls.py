from django.urls import path
from . import views

urlpatterns = [
    path('quizzes/', views.QuizListView.as_view(), name='quiz_list'),
    path('quizzes/<int:pk>/', views.QuizDetailView.as_view(), name='quiz_detail'),
    path('questions/', views.QuestionListView.as_view(), name='question_list'),
    path('questions/<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('exams/', views.ExamListView.as_view(), name='exam_list'),
    path('exams/<int:pk>/', views.ExamDetailView.as_view(), name='exam_detail'),
    path('quizzes/create/', views.QuizCreateView.as_view(), name='quiz_create'),
    path('questions/create/', views.QuestionCreateView.as_view(), name='question_create'),
    path('exams/create/', views.ExamCreateView.as_view(), name='exam_create'),
]