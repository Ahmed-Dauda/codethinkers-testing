from django.urls import path
from . import views

urlpatterns = [
    path('programs/', views.async_program_pages_list_view, name='program_pages_list'),
    path("test-speed/", views.test_async_speed, name="test_async_speed"),

    path("test-fastapi/", views.test_fastapi, name="test_fastapi"),

]
