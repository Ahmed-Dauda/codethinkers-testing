from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('hospital.urls')),  # App at root
    path('admin/', admin.site.urls),
]
