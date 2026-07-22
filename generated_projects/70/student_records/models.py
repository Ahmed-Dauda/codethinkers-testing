from django.db import models

class Student(models.Model):
    full_name = models.CharField(max_length=255)
    admission_number = models.CharField(max_length=100, unique=True)
    class_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    parent_phone = models.CharField(max_length=15)

    def __str__(self):
        return self.full_name