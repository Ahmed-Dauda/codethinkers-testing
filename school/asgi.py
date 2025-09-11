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
from starlette.middleware.wsgi import WSGIMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

# Create FastAPI app
fastapi_app = FastAPI()

@fastapi_app.get("/fastapi/api/hello")
async def hello(name: str = "World"):
    return {"message": f"Hello, {name} from FastAPI!"}

# Mount Django as ASGI
django_asgi_app = get_asgi_application()

# Main app that includes both
from starlette.middleware.wsgi import WSGIMiddleware
from starlette.routing import Mount
from starlette.applications import Starlette

application = Starlette(routes=[
    Mount("/fastapi", app=fastapi_app),
    Mount("/", app=django_asgi_app),  # Django at root
])
