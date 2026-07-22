from django.db import models

class PosAttendant(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

class SalesRecord(models.Model):
    attendant = models.ForeignKey(PosAttendant, on_delete=models.CASCADE)
    date = models.DateField()
    total_sales = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.attendant.name} - {self.total_sales} on {self.date}'