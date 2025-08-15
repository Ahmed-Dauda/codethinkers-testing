# admin.py
from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from django.urls import reverse
from urllib.parse import urlencode

from .models import CourseCertificateCount, CertificateDownload


@admin.register(CourseCertificateCount)
class CourseCertificateCountAdmin(admin.ModelAdmin):
    # Show "TITLE COUNT" and make it clickable to see the underlying downloads
    list_display = ('title_with_count', 'created_at')
    search_fields = ('title',)
    ordering = ('-created_at',)

    def get_queryset(self, request):
        # Annotate with downloads count for performance
        qs = super().get_queryset(request)
        return qs.annotate(downloads_count=Count('downloads'))

    def title_with_count(self, obj):
        # Fallback if annotation missing
        count = getattr(obj, 'downloads_count', obj.downloads.count())
        # Link to the CertificateDownload changelist filtered by this certificate
        url = (
            reverse('admin:certificate_stats_certificatedownload_changelist')
            + "?"
            + urlencode({'certificate__id__exact': obj.id})
        )
        return format_html('<a href="{}">{} {}</a>', url, obj.title.upper(), count)

    title_with_count.short_description = "Certificate (Downloads)"


@admin.register(CertificateDownload)
class CertificateDownloadAdmin(admin.ModelAdmin):
    list_display = ('certificate', 'user', 'downloaded_at')
    list_filter = ('certificate', 'downloaded_at')
    search_fields = ('certificate__title', 'user__username', 'user__email')
    ordering = ('-downloaded_at',)
