"""
ASGI config for school project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')

application = get_asgi_application()


# import os
# from django.core.asgi import get_asgi_application
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.wsgi import WSGIMiddleware
# from starlette.routing import Mount
# from starlette.applications import Starlette

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school.settings")

# # Django ASGI application
# django_asgi_app = get_asgi_application()

# # FastAPI application
# fastapi_app = FastAPI(title="Codethinkers AI API")

# # Allow CORS (for React or other frontends)
# fastapi_app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # change to your domain in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Example FastAPI route
# @fastapi_app.get("/welcome")
# async def welcome():
#     return {"message": "Welcome to Codethinkers Academy 🚀"}

# # Mount Django and FastAPI together
# application = Starlette(routes=[
#     Mount("/", app=WSGIMiddleware(django_asgi_app)),  # Django handles main routes
#     Mount("/api", app=fastapi_app)  # FastAPI mounted under /api
# ])
