from django.urls import path
from . import views

app_name = 'expense_tracker'

urlpatterns = [
    path('', views.IncomeListView.as_view(), name='home'),
    path('income/', views.IncomeListView.as_view(), name='income_list'),
    path('income/add/', views.IncomeCreateView.as_view(), name='income_add'),
    path('income/edit/<int:pk>/', views.IncomeUpdateView.as_view(), name='income_edit'),
    path('income/delete/<int:pk>/', views.IncomeDeleteView.as_view(), name='income_delete'),
    path('expense/', views.ExpenseListView.as_view(), name='expense_list'),
    path('expense/add/', views.ExpenseCreateView.as_view(), name='expense_add'),
    path('expense/edit/<int:pk>/', views.ExpenseUpdateView.as_view(), name='expense_edit'),
    path('expense/delete/<int:pk>/', views.ExpenseDeleteView.as_view(), name='expense_delete'),
]