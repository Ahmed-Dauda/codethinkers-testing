from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Income, Expense, Category

class HomeView(TemplateView):
    template_name = 'home.html'

class IncomeListView(ListView):
    model = Income
    paginate_by = 25
    def get_queryset(self):
        return super().get_queryset().select_related('category').order_by('-date')

class ExpenseListView(ListView):
    model = Expense
    paginate_by = 25
    def get_queryset(self):
        return super().get_queryset().select_related('category').order_by('-date')

class CategoryListView(ListView):
    model = Category
    paginate_by = 25

class IncomeCreateView(CreateView):
    model = Income
    fields = '__all__'
    success_url = '/'

class ExpenseCreateView(CreateView):
    model = Expense
    fields = '__all__'
    success_url = '/'

class IncomeUpdateView(UpdateView):
    model = Income
    fields = '__all__'
    success_url = '/'

class ExpenseUpdateView(UpdateView):
    model = Expense
    fields = '__all__'
    success_url = '/'