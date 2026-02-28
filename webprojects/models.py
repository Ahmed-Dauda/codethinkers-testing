from django.db import models
from sms.models import Courses, Topics, Categories
from users.models import NewUser as User
from cloudinary.models import CloudinaryField
import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


# ---------------- Helper ----------------
# def get_general_topic(course):
#     if not course:
#         return None

#     general_topic, _ = Topics.objects.get_or_create(
#         title="General",
#         courses=course,
#         defaults={
#             "categories": course.categories if course.categories else None
#         }
#     )
#     return general_topic


# ---------------- Project ----------------

class Project(models.Model):
    name   = models.CharField(max_length=100)
    course = models.ForeignKey(
        'sms.Courses',            # ← explicit app.Model string avoids mis-resolution
        on_delete=models.CASCADE,
        null=True,
        related_name="projects"
    )
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(
        'sms.Topics',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return f"/webprojects/{self.id}/"

    def __str__(self):
        return f"{self.name} (ID: {self.id})"


# ---------------- Folder ----------------
class Folder(models.Model):
    project = models.ForeignKey(Project, related_name="folders", on_delete=models.CASCADE)
    name    = models.CharField(max_length=100)
    parent  = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    topic   = models.ForeignKey(
        'sms.Topics',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        parent_name = f" > {self.parent.name}" if self.parent else ""
        return f"{self.name}{parent_name} (Folder ID: {self.id})"


# ---------------- File ----------------
class File(models.Model):

    current_topic = models.ForeignKey(
        'sms.Topics',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_files',
        help_text="Which lesson is this file for?"
    )
    project = models.ForeignKey(
        Project,
        null=True,
        blank=True,
        default=None,
        related_name="files",
        on_delete=models.CASCADE
    )
    folder = models.ForeignKey(
        Folder,
        null=True,
        blank=True,
        related_name="files",
        on_delete=models.CASCADE
    )
    topic = models.ForeignKey(
        'sms.Topics',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_files"
    )

    name    = models.CharField(max_length=300)
    content = models.TextField(blank=True)

    image = CloudinaryField('image', blank=True, null=True)
    file  = models.FileField(upload_to='uploads/', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (File ID: {self.id}) — Project: {self.project.name}"

    def extension(self):
        return self.name.split('.')[-1].lower()

    def is_python(self):  return self.name.lower().endswith(".py")
    def is_css(self):     return self.extension() == "css"
    def is_js(self):      return self.extension() == "js"
    def is_html(self):    return self.extension() in ["html", "htm"]
    def is_image(self):   return self.extension() in ["jpg", "jpeg", "png", "gif", "svg", "webp"]
    def is_excel(self):   return self.extension() in ["xls", "xlsx", "csv"]

    def file_url(self):
        if self.image: return self.image.url
        if self.file:  return self.file.url
        return ""


# ---------------- XP & Progress ----------------

class StudentXP(models.Model):
    student     = models.OneToOneField(User, on_delete=models.CASCADE)
    total_xp    = models.IntegerField(default=0)
    streak_days = models.IntegerField(default=0)
    last_active = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} — {self.total_xp}XP"


class StudentProgress(models.Model):
    student          = models.ForeignKey(User, on_delete=models.CASCADE)
    course           = models.ForeignKey('sms.Courses', on_delete=models.CASCADE, null=True, blank=True)
    current_topic    = models.ForeignKey('sms.Topics', on_delete=models.SET_NULL, null=True, blank=True)
    completed_topics = models.ManyToManyField('sms.Topics', related_name='completed_by_students', blank=True)
    last_updated     = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'course')

    @classmethod
    def get_for_student(cls, user):
        progress, _ = cls.objects.get_or_create(student=user, course=None)
        return progress


# ---------------- Signals ----------------

@receiver(post_delete, sender=File)
def delete_file_on_model_delete(sender, instance, **kwargs):
    if instance.file and os.path.isfile(instance.file.path):
        os.remove(instance.file.path)


# @receiver(pre_save, sender=Project)
# def set_project_topic(sender, instance, **kwargs):
#     if not instance.topic and instance.course:
#         instance.topic = get_general_topic(instance.course)


# @receiver(pre_save, sender=Folder)
# def set_folder_topic(sender, instance, **kwargs):
#     if not instance.topic and instance.project:
#         instance.topic = get_general_topic(instance.project.course)


# @receiver(pre_save, sender=File)
# def set_file_topic(sender, instance, **kwargs):
#     if not instance.topic and instance.project and instance.project.course:
#         instance.topic = get_general_topic(instance.project.course)