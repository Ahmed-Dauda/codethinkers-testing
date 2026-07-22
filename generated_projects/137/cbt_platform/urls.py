from django.contrib import admin
admin.site.site_header = 'Cbt Platform Admin'
admin.site.site_title = 'Cbt Platform'
admin.site.index_title = 'Dashboard'

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('cbt_platform_app.urls')),  # App at root
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
