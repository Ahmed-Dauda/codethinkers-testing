from django.db import models

class Exam(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    duration = models.DurationField()
    total_marks = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.title