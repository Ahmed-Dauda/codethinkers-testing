from django.views.generic import ListView, DetailView
from .models import Staff, Department

class HomeView(ListView):
    template_name = 'home.html'
    model = Staff
    context_object_name = 'staff_list'
    paginate_by = 25

    def get_queryset(self):
        return super().get_queryset().select_related('department').order_by('-id')

class StaffListView(ListView):
    template_name = 'staff_list.html'
    model = Staff
    context_object_name = 'staff_list'
    paginate_by = 25

    def get_queryset(self):
        return super().get_queryset().select_related('department').order_by('-id')

class StaffDetailView(DetailView):
    template_name = 'staff_detail.html'
    model = Staff
    context_object_name = 'staff'

class DepartmentListView(ListView):
    template_name = 'department_list.html'
    model = Department
    context_object_name = 'department_list'
    paginate_by = 25

class DepartmentDetailView(DetailView):
    template_name = 'department_detail.html'
    model = Department
    context_object_name = 'department'