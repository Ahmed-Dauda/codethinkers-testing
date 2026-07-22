from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('blog.urls')),  # App at root
    path('admin/', admin.site.urls),
]
