from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.urls import reverse_lazy
from .models import Employee, Department

class HomeView(ListView):
    template_name = 'home.html'
    def get_queryset(self):
        return Employee.objects.all().order_by('-id')

class EmployeeListView(ListView):
    model = Employee
    template_name = 'employee_list.html'
    context_object_name = 'employees'
    ordering = ['-id']

class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'employee_detail.html'

class EmployeeCreateView(CreateView):
    model = Employee
    template_name = 'employee_form.html'
    fields = '__all__'

class EmployeeUpdateView(UpdateView):
    model = Employee
    template_name = 'employee_form.html'
    fields = '__all__'

class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'employee_confirm_delete.html'
    success_url = reverse_lazy('employee_management_app:home')

class CheckInView(UpdateView):
    model = Employee
    template_name = 'employee_form.html'  # ← ADD THIS
    fields = []
    success_url = reverse_lazy('employee_management_app:home')  # ← ADD THIS
    
    def form_valid(self, form):
        form.instance.check_in_time = timezone.now()
        return super().form_valid(form)

class CheckOutView(UpdateView):
    model = Employee
    template_name = 'employee_form.html'  # ← ADD THIS
    fields = []
    success_url = reverse_lazy('employee_management_app:home')  # ← ADD THIS
    
    def form_valid(self, form):
        form.instance.check_out_time = timezone.now()
        return super().form_valid(form)