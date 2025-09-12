"""
ASGI config for school project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')

# application = get_asgi_application()


# asgi.py
from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware
from starlette.applications import Starlette
from starlette.routing import Mount
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()
fastapi_app = FastAPI()

@fastapi_app.get("/welcome")
async def welcome():
    return {"message": "Welcome to Codethinkers Academy 🚀"}

application = Starlette(routes=[
    Mount("/", app=WSGIMiddleware(django_asgi_app)),
    Mount("/api", app=fastapi_app)  # mounted under /api
])
