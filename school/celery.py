<<<<<<< HEAD
# school/celery.py
=======
>>>>>>> f7f0302b0f654bf25ed1566c5dcb826ef34d7325
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')

app = Celery('school')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
<<<<<<< HEAD

# Windows fix
import sys
if sys.platform == 'win32':
    app.conf.worker_pool = 'solo'
=======
>>>>>>> f7f0302b0f654bf25ed1566c5dcb826ef34d7325
