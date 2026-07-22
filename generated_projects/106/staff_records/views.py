from django.views.generic import ListView
from .models import Employee, Department

class HomeView(ListView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee_count'] = Employee.objects.count()
        context['department_count'] = Department.objects.count()
        return context