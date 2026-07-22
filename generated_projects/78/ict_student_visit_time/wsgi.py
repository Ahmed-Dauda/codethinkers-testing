import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ict_student_visit_time.settings")

application = get_wsgi_application()
