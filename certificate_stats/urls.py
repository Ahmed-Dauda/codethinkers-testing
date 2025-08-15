from django.urls import path
from . import views

urlpatterns = [
    path('downloads/courses/', views.course_download_counts, name='course_download_counts'),
    path('stats/', views.CertificateDownload, name='certificate_download_stats'),
]
