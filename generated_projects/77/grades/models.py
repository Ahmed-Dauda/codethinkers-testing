from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    ca = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0)
    exam = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0)  # Updated to allow null and blank
    total = models.DecimalField(max_digits=5, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total = self.ca + self.exam if self.ca is not None else self.exam
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name