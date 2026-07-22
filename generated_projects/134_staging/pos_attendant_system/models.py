from django.db import models

class SalesRecord(models.Model):
    attendant_name = models.CharField(max_length=255)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.attendant_name} - {self.total_sales} on {self.date}'