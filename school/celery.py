# school/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')

app = Celery('school')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Windows fix
import sys
if sys.platform == 'win32':
    app.conf.worker_pool = 'solo'