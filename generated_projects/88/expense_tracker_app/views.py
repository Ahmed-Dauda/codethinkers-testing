from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Expense, Income, Category


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_expenses'] = Expense.objects.filter(user=self.request.user).aggregate(total=models.Sum('amount'))['total'] or 0
        context['total_income'] = Income.objects.filter(user=self.request.user).aggregate(total=models.Sum('amount'))['total'] or 0
        context['total_categories'] = Category.objects.count()
        return context


class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    paginate_by = 25

    def get_queryset(self):
        return super().get_queryset().select_related('category').filter(user=self.request.user).order_by('-date')


class IncomeListView(LoginRequiredMixin, ListView):
    model = Income
    paginate_by = 25

    def get_queryset(self):
        return super().get_queryset().select_related('category').filter(user=self.request.user).order_by('-date')


class CategoryListView(ListView):
    # No user-specific filtering here, so no login required — remove
    # LoginRequiredMixin if you want categories to be shared/public,
    # or add it back if categories should also be private per user.
    model = Category
    paginate_by = 25


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    fields = ['category', 'amount', 'description', 'date']
    success_url = reverse_lazy('expense_tracker:expense_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class IncomeCreateView(LoginRequiredMixin, CreateView):
    model = Income
    fields = ['category', 'amount', 'description', 'date']
    success_url = reverse_lazy('expense_tracker:income_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)