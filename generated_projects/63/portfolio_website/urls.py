from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Project is running! Visit /admin/ for admin panel.")

urlpatterns = [
    path('', include('portfolio.urls')),  # App at root
    path('', home, name='home'),
    path('admin/', admin.site.urls),
]
