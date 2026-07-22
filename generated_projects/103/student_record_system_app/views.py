from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Student, Attendance, Grade

class HomeView(ListView):
    template_name = 'home.html'
    model = Student
    context_object_name = 'students'
    paginate_by = 25

class StudentListView(ListView):
    template_name = 'student_list.html'
    model = Student
    context_object_name = 'students'
    paginate_by = 25

class StudentDetailView(DetailView):
    template_name = 'student_detail.html'
    model = Student

class AttendanceListView(ListView):
    template_name = 'attendance_list.html'
    model = Attendance
    context_object_name = 'attendances'
    paginate_by = 25

class AttendanceDetailView(DetailView):
    template_name = 'attendance_detail.html'
    model = Attendance

class GradeListView(ListView):
    template_name = 'grade_list.html'
    model = Grade
    context_object_name = 'grades'
    paginate_by = 25

class GradeDetailView(DetailView):
    template_name = 'grade_detail.html'
    model = Grade