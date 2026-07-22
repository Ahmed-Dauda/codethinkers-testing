from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Student
from .forms import StudentForm

class StudentListView(ListView):
    model = Student
    template_name = 'student_list.html'
    paginate_by = 25

class StudentDetailView(DetailView):
    model = Student
    template_name = 'student_detail.html'

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_form.html'
    success_url = '/students/'

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_form.html'
    success_url = '/students/'

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_confirm_delete.html'
    success_url = '/students/'