from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField()
    image = models.ImageField(upload_to='project_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']

class Experience(models.Model):
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='experience_images/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.job_title

    class Meta:
        ordering = ['-id']

class About(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    comment = models.TextField(null=True, blank=True)  # New comment field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']

class Comment(models.Model):
    content = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment on {self.project or self.experience}'

    class Meta:
        ordering = ['-created_at']