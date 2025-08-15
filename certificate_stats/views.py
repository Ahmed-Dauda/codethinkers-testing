# certificate_stats/views.py
from django.shortcuts import get_object_or_404, render
from django.http import FileResponse
from django.db.models import Count
from .models import CourseCertificateCount, CertificateDownload
from quiz.models import Course  # adjust to your structure

def download_certificate(request, certificate_id):
    certificate = get_object_or_404(CourseCertificateCount, id=certificate_id)

    # Log the download
    CertificateDownload.objects.create(
        certificate=certificate,
        user=request.user if request.user.is_authenticated else None
    )

    return FileResponse(certificate.file.open('rb'), as_attachment=True, filename=certificate.file.name)


def course_download_counts(request):
    courses = (
        Course.objects
        .annotate(downloads=Count('certificate_count__downloads'))  # Adjust "certificate_count" to match your FK related_name
        .order_by('-downloads', 'course_name')
    )
    return render(
        request,
        'certificate_stats/course_download_counts.html',
        {'courses': courses}
    )


