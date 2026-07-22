from django.urls import path
from .views import HomeView

app_name = 'staff_records'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]