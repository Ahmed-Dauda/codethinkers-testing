from django.views.generic import ListView
from django.db.models import Sum
from .models import Sale, Expense, Category

class HomeView(ListView):
    model = Sale
    template_name = 'home.html'
    context_object_name = 'sales'
    paginate_by = 25

    def get_queryset(self):
        return super().get_queryset().select_related('attendant', 'category').order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_revenue = Sale.objects.aggregate(total=Sum('amount'))['total'] or 0
        total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
        context['total_revenue'] = total_revenue
        context['total_expenses'] = total_expenses
        context['net_revenue'] = total_revenue - total_expenses
        return context