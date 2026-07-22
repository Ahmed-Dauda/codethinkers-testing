from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Question, Result

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class QuizListView(ListView):
    model = Question
    template_name = 'quiz_list.html'
    context_object_name = 'quizzes'
    paginate_by = 25

class QuizDetailView(DetailView):
    model = Question
    template_name = 'quiz_detail.html'
    context_object_name = 'quiz'

class AttemptCreateView(LoginRequiredMixin, CreateView):
    model = Result
    template_name = 'attempt_form.html'
    fields = ['question', 'score']
    success_url = '/'  # Redirect after successful attempt

    def form_valid(self, form):
        form.instance.user = self.request.user  # Associate attempt with logged-in user
        return super().form_valid(form)
