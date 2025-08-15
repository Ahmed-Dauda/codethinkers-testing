# tasks.py
from django.utils import timezone
from datetime import timedelta
from .models import UserStatus

def update_user_status():
    now = timezone.now()
    timeout = timedelta(minutes=5)
    UserStatus.objects.filter(last_seen__lt=now - timeout).update(is_online=False)
