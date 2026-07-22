from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Employee, Department

class HomeView(ListView):
    template_name = 'home.html'
    model = Employee
    context_object_name = 'employees'
    paginate_by = 25

    def get_queryset(self):
        return super().get_queryset().select_related('department').order_by('-id')

class EmployeeListView(ListView):
    template_name = 'employee_list.html'
    model = Employee
    context_object_name = 'employees'
    paginate_by = 25

    def get_queryset(self):
        return super().get_queryset().select_related('department').order_by('-id')

class EmployeeDetailView(DetailView):
    template_name = 'employee_detail.html'
    model = Employee

class EmployeeCreateView(CreateView):
    template_name = 'employee_create.html'
    model = Employee
    fields = ['first_name', 'last_name', 'department']
    success_url = '/employees/'  # Update with the correct URL

class EmployeeUpdateView(UpdateView):
    template_name = 'employee_update.html'
    model = Employee
    fields = ['first_name', 'last_name', 'department']
    success_url = '/employees/'  # Update with the correct URL

class EmployeeDeleteView(DeleteView):
    template_name = 'employee_delete.html'
    model = Employee
    success_url = '/employees/'  # Update with the correct URL

class DepartmentListView(ListView):
    template_name = 'department_list.html'
    model = Department
    context_object_name = 'departments'
    paginate_by = 25

class DepartmentDetailView(DetailView):
    template_name = 'department_detail.html'
    model = Department

class DepartmentCreateView(CreateView):
    template_name = 'department_create.html'
    model = Department
    fields = ['name']
    success_url = '/departments/'  # Update with the correct URL

class DepartmentUpdateView(UpdateView):
    template_name = 'department_update.html'
    model = Department
    fields = ['name']
    success_url = '/departments/'  # Update with the correct URL

class DepartmentDeleteView(DeleteView):
    template_name = 'department_delete.html'
    model = Department
    success_url = '/departments/'  # Update with the correct URL