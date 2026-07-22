import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "give_me_the_prompt_let_me_try_it_again.settings")

application = get_wsgi_application()
