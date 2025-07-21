# editor/models.py
from django.db import models
from users.models import NewUser as User
from cloudinary.models import CloudinaryField  # Make sure this is installed and configured


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
    name = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    image = CloudinaryField('image', blank=True, null=True)  # for uploaded images
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def extension(self):
        return self.name.split('.')[-1].lower()

    def is_css(self):
        return self.extension() == "css"

    def is_js(self):
        return self.extension() == "js"

    def is_image(self):
        return self.extension() in ["jpg", "jpeg", "png", "gif", "svg", "webp"]

    def is_html(self):
        return self.extension() in ["html", "htm"]

    def __str__(self):
        return f"{self.name} (File ID: {self.id}) — Project: {self.project.name}"
    