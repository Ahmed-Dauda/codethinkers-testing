from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),  # Home page with dashboard
    path('quizzes/', views.QuizListView.as_view(), name='quiz_list'),  # List of available quizzes
    path('quizzes/<int:pk>/', views.QuizDetailView.as_view(), name='quiz_detail'),  # Detail view for a specific quiz
    path('attempts/new/', views.AttemptCreateView.as_view(), name='attempt_create'),  # Form to submit a new attempt
]