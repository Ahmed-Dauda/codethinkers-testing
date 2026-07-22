from django.contrib import admin
admin.site.site_header = 'Library Management System Admin'
admin.site.site_title = 'Library Management System'
admin.site.index_title = 'Dashboard'

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('library_management.urls')),  # App at root
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
