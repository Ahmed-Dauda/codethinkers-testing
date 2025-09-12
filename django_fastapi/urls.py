from django.urls import path
from . import views

urlpatterns = [
    path("test-fastapi/", views.test_fastapi_async, name="test_fastapi"),
    path('frontend/', views.frontend, name='frontend'),
    path("proxy/test-ai/", views.proxy_fastapi_test, name="proxy_fastapi_test"),
    
]
