from django.test import TestCase
from .models import Income, Expense, Category

class ExpenseTrackerTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Food')
        self.income = Income.objects.create(amount=1000, date='2023-01-01', category=self.category)
        self.expense = Expense.objects.create(amount=200, date='2023-01-02', category=self.category)

    def test_income_creation(self):
        self.assertEqual(self.income.amount, 1000)
        self.assertEqual(self.income.category.name, 'Food')

    def test_expense_creation(self):
        self.assertEqual(self.expense.amount, 200)
        self.assertEqual(self.expense.category.name, 'Food')