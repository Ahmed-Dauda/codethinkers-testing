from django.db import models
from django.conf import settings

class CourseCertificateCount(models.Model):
    title = models.CharField(max_length=255)  # e.g., "Python Course Completion"
    file = models.FileField(upload_to='certificates/', blank=True, null=True)  # optional, to store file
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CertificateDownload(models.Model):
    certificate = models.ForeignKey(CourseCertificateCount, on_delete=models.CASCADE, related_name='downloads')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    downloaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} downloaded {self.certificate} on {self.downloaded_at}"

# models.py
from django.db import models
from django.utils import timezone
from django.conf import settings

class UserStatus(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_seen = models.DateTimeField(default=timezone.now)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {'Online' if self.is_online else 'Offline'}"
