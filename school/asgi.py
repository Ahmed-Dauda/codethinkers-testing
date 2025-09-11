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


import os
import django
from django.core.asgi import get_asgi_application
from fastapi import FastAPI, Request
from django.urls import path
from django.http import JsonResponse
from starlette.middleware.wsgi import WSGIMiddleware
from starlette.applications import Starlette

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yourproject.settings")
django.setup()

# Django ASGI app
django_app = get_asgi_application()

# FastAPI app
fastapi_app = FastAPI()

# ✅ Add /generate endpoint
@fastapi_app.get("/generate")
async def generate(name: str = "World"):
    return {"message": f"Hello, {name}!"}

# Combine Django + FastAPI
application = Starlette()
application.mount("/", WSGIMiddleware(django_app))  # Django handles normal routes
application.mount("/", fastapi_app)                 # FastAPI also mounted at root
