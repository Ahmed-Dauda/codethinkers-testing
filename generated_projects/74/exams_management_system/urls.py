from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('exams.urls')),  # App at root
    path('admin/', admin.site.urls),
]
