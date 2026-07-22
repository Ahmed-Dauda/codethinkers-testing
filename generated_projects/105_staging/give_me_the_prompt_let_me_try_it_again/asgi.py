import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "give_me_the_prompt_let_me_try_it_again.settings")

application = get_asgi_application()
