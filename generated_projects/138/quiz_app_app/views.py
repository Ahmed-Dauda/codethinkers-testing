from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Quiz, Question, Exam

class QuizListView(ListView):
    model = Quiz
    template_name = 'quiz_list.html'
    paginate_by = 25

    def get_queryset(self):
        return super().get_queryset().order_by('-id')

class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz_detail.html'

class QuestionListView(ListView):
    model = Question
    template_name = 'question_list.html'
    paginate_by = 25

    def get_queryset(self):
        return super().get_queryset().order_by('-id')

class QuestionDetailView(DetailView):
    model = Question
    template_name = 'question_detail.html'

class ExamListView(ListView):
    model = Exam
    template_name = 'exam_list.html'
    paginate_by = 25

    def get_queryset(self):
        return super().get_queryset().order_by('-id')

class ExamDetailView(DetailView):
    model = Exam
    template_name = 'exam_detail.html'

class QuizCreateView(CreateView):
    model = Quiz
    fields = ['title', 'description']
    template_name = 'quiz_form.html'
    success_url = '/quizzes/'  # Adjust as necessary

class QuestionCreateView(CreateView):
    model = Question
    fields = ['quiz', 'text']
    template_name = 'question_form.html'
    success_url = '/questions/'  # Adjust as necessary

class ExamCreateView(CreateView):
    model = Exam
    fields = ['quiz', 'date', 'duration']
    template_name = 'exam_form.html'
    success_url = '/exams/'  # Adjust as necessary