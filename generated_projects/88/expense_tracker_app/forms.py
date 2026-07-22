from django import forms
from .models import Expense, Income

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = '__all__'