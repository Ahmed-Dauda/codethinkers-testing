from django.urls import path
from . import views

app_name = 'cbt'

urlpatterns = [
    path('', views.QuizListView.as_view(), name='quiz_list'),  # List of all quizzes
    path('quiz/<int:pk>/', views.QuizDetailView.as_view(), name='quiz_detail'),  # Detail view for a specific quiz
    path('quiz/<int:quiz_id>/submit/', views.SubmitAnswerView.as_view(), name='submit_answer'),  # Submit answers for a quiz
    path('question/', views.QuestionListView.as_view(), name='question_list'),  # List of all questions
]