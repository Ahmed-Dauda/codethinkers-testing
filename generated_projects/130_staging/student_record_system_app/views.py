from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Student, Course, Enrollment

class StudentListView(ListView):
    template_name = 'student_list.html'
    model = Student
    paginate_by = 25

    def get_queryset(self):
        return super().get_queryset().order_by('-id')

class StudentDetailView(DetailView):
    template_name = 'student_detail.html'
    model = Student

class StudentCreateView(CreateView):
    template_name = 'student_create.html'
    model = Student
    fields = ['first_name', 'last_name', 'email']
    success_url = '/students/'  # Adjust as necessary

class StudentUpdateView(UpdateView):
    template_name = 'student_update.html'
    model = Student
    fields = ['first_name', 'last_name', 'email']
    success_url = '/students/'  # Adjust as necessary

class StudentDeleteView(DeleteView):
    template_name = 'student_delete.html'
    model = Student
    success_url = '/students/'  # Adjust as necessary

class CourseListView(ListView):
    template_name = 'course_list.html'
    model = Course
    paginate_by = 25

    def get_queryset(self):
        return super().get_queryset().order_by('-id')

class CourseDetailView(DetailView):
    template_name = 'course_detail.html'
    model = Course

class CourseCreateView(CreateView):
    template_name = 'course_create.html'
    model = Course
    fields = ['name', 'description']
    success_url = '/courses/'  # Adjust as necessary

class CourseUpdateView(UpdateView):
    template_name = 'course_update.html'
    model = Course
    fields = ['name', 'description']
    success_url = '/courses/'  # Adjust as necessary

class CourseDeleteView(DeleteView):
    template_name = 'course_delete.html'
    model = Course
    success_url = '/courses/'  # Adjust as necessary

class EnrollmentListView(ListView):
    template_name = 'enrollment_list.html'
    model = Enrollment
    paginate_by = 25

    def get_queryset(self):
        return super().get_queryset().order_by('-id')

class EnrollmentDetailView(DetailView):
    template_name = 'enrollment_detail.html'
    model = Enrollment

class EnrollmentCreateView(CreateView):
    template_name = 'enrollment_create.html'
    model = Enrollment
    fields = ['student', 'course']
    success_url = '/enrollments/'  # Adjust as necessary

class EnrollmentUpdateView(UpdateView):
    template_name = 'enrollment_update.html'
    model = Enrollment
    fields = ['student', 'course']
    success_url = '/enrollments/'  # Adjust as necessary

class EnrollmentDeleteView(DeleteView):
    template_name = 'enrollment_delete.html'
    model = Enrollment
    success_url = '/enrollments/'  # Adjust as necessary