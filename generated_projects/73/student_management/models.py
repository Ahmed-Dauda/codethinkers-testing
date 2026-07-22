from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    class_enrolled = models.ForeignKey('Class', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Class(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'