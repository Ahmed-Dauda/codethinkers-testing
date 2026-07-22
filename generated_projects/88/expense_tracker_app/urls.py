from django.urls import path
from . import views

app_name = 'expense_tracker'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('expenses/', views.ExpenseListView.as_view(), name='expense_list'),
    path('incomes/', views.IncomeListView.as_view(), name='income_list'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('expenses/add/', views.ExpenseCreateView.as_view(), name='expense_create'),
    path('incomes/add/', views.IncomeCreateView.as_view(), name='income_create'),
]