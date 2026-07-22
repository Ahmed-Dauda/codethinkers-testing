from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Income, Expense, Category

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

class IncomeDeleteView(DeleteView):
    model = Income
    success_url = '/'

class ExpenseDeleteView(DeleteView):
    model = Expense
    success_url = '/'