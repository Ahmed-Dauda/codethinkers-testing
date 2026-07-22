from django.db import models

class Attendant(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Sale(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    date = models.DateField(auto_now_add=True, db_index=True)
    attendant = models.ForeignKey(Attendant, on_delete=models.CASCADE, related_name='sales')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sales')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'Sale on {self.date}: ${self.amount} by {self.attendant}'

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    date = models.DateField(auto_now_add=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'Expense on {self.date}: ${self.amount}'