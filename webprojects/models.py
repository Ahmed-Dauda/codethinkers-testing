# editor/models.py
from django.db import models
from users.models import NewUser as User
from cloudinary.models import CloudinaryField  # Make sure this is installed and configured
import os
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Project(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return f"/webprojects/{self.id}/"

    def __str__(self):
        return f"{self.name} (ID: {self.id})"

class Folder(models.Model):
    project = models.ForeignKey(Project, related_name="folders", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        parent_name = f" > {self.parent.name}" if self.parent else ""
        return f"{self.name}{parent_name} (Folder ID: {self.id})"


class File(models.Model):
    project = models.ForeignKey(Project, related_name="files", on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, null=True, blank=True, related_name="files", on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    content = models.TextField(blank=True)

    # Support images via Cloudinary
    image = CloudinaryField('image', blank=True, null=True)

    # Support any file (Excel, CSV, PDF, etc.)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def is_frontend(self):
        return self.folder and self.folder.name == "frontend"

    def is_backend(self):
        return self.folder and self.folder.name == "backend"

    # --- Helpers ---
    def extension(self):
        return self.name.split('.')[-1].lower()
    
   
    def is_python(self):
        return self.name.lower().endswith(".py")

    def is_css(self):
        return self.extension() == "css"

    def is_js(self):
        return self.extension() == "js"

    def is_image(self):
        return self.extension() in ["jpg", "jpeg", "png", "gif", "svg", "webp"]

    def is_html(self):
        return self.extension() in ["html", "htm"]

    def is_excel(self):
        return self.extension() in ["xls", "xlsx", "csv"]

    def file_url(self):
        """Return correct URL whether it's an image or a general file."""
        if self.image:
            return self.image.url
        if self.file:
            return self.file.url
        return ""

    def __str__(self):
        return f"{self.name} (File ID: {self.id}) — Project: {self.project.name}"


@receiver(post_delete, sender=File)
def delete_file_on_model_delete(sender, instance, **kwargs):
    if instance.file and os.path.isfile(instance.file.path):
        os.remove(instance.file.path)


# class File(models.Model):
#     project = models.ForeignKey(Project, related_name="files", on_delete=models.CASCADE)
#     folder = models.ForeignKey(Folder, null=True, blank=True, related_name="files", on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     content = models.TextField(blank=True)
#     image = CloudinaryField('image', blank=True, null=True)  # for uploaded images
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def extension(self):
#         return self.name.split('.')[-1].lower()

#     def is_css(self):
#         return self.extension() == "css"

#     def is_js(self):
#         return self.extension() == "js"

#     def is_image(self):
#         return self.extension() in ["jpg", "jpeg", "png", "gif", "svg", "webp"]

#     def is_html(self):
#         return self.extension() in ["html", "htm"]

#     def __str__(self):
#         return f"{self.name} (File ID: {self.id}) — Project: {self.project.name}"
    