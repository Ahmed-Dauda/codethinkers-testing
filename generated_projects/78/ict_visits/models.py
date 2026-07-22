from django.db import models

class StudentVisit(models.Model):
    student_name = models.CharField(max_length=100)
    visit_time = models.DateTimeField()
    purpose = models.TextField()

    def __str__(self):
        return self.student_name