from django.urls import path
from .views import HomeView

app_name = 'student_portal_app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]