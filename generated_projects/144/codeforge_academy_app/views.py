from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Course, Enrollment, Progress

class HomeView(ListView):
    template_name = 'home.html'
    def get_queryset(self):
        return Enrollment.objects.all()  # Example for enrollment stats

class CourseListView(ListView):
    model = Course
    template_name = 'course_list.html'
    paginate_by = 25

class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_detail.html'

class EnrollmentCreateView(CreateView):
    model = Enrollment
    fields = ['student', 'course']
    template_name = 'enrollment_form.html'
    success_url = reverse_lazy('course_list')

class ProgressUpdateView(UpdateView):
    model = Progress
    fields = ['completed', 'grade']
    template_name = 'progress_form.html'
    success_url = reverse_lazy('course_list')