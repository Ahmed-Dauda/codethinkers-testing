from django.views.generic import TemplateView
from django.db.models import Count
from .models import Student, Course, Progress

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_count'] = Student.objects.count()
        context['course_count'] = Course.objects.count()
        context['progress_count'] = Progress.objects.count()
        return context