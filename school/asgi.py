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
from fastapi import FastAPI
from django.urls import path
from django.http import JsonResponse
from starlette.middleware.wsgi import WSGIMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school.settings")
django.setup()

# Django ASGI app
django_app = get_asgi_application()

# FastAPI app
fastapi_app = FastAPI()

@fastapi_app.get("/api/hello")
async def hello(name: str = "World"):
    return {"message": f"Hello, {name}!"}

# Combine Django + FastAPI
from starlette.applications import Starlette

application = Starlette()
application.mount("/", WSGIMiddleware(django_app))       # Django handles normal routes
application.mount("/fastapi", fastapi_app)               # FastAPI under /fastapi/*
