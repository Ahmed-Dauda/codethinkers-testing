from django.db import models

class Hero(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    subtitle = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='hero_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

class AboutMe(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

class Skill(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    proficiency = models.IntegerField(default=0)  # 0-100 scale
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    link = models.URLField()
    image = models.ImageField(upload_to='project_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

class Experience(models.Model):
    job_title = models.CharField(max_length=200, db_index=True)
    company = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.job_title

class ContactFormSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name