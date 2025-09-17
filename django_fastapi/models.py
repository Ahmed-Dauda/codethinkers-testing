from django.db import models

# Create your models here.
class ProgramPage(models.Model):
    title = models.CharField(max_length=255)
    # subtitle = models.CharField(max_length=255)
    description = models.TextField()
    # cta_text = models.CharField(max_length=50)
    benefits = models.TextField()  # List of benefits

    def __str__(self):
        return self.title

    def get_benefits_list(self):
        return self.benefits.splitlines()