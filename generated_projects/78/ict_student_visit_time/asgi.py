import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ict_student_visit_time.settings")

application = get_asgi_application()
