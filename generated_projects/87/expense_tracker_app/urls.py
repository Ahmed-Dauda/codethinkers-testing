from django.urls import path
from . import views

app_name = 'expense_tracker'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('income/', views.IncomeListView.as_view(), name='income_list'),
    path('expense/', views.ExpenseListView.as_view(), name='expense_list'),
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('income/create/', views.IncomeCreateView.as_view(), name='income_create'),
    path('expense/create/', views.ExpenseCreateView.as_view(), name='expense_create'),
    path('income/update/<int:pk>/', views.IncomeUpdateView.as_view(), name='income_update'),
    path('expense/update/<int:pk>/', views.ExpenseUpdateView.as_view(), name='expense_update'),
]