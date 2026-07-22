from django.shortcuts import render
from django.http import HttpResponse
from .models import StudentVisit
import csv


def home(request):
    objects = StudentVisit.objects.all().order_by('-id')
    return render(request, 'list.html', {'objects': objects})


def export_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_visits.csv"'

    writer = csv.writer(response)
    writer.writerow(['Student Name', 'Visit Time', 'Purpose'])

    visits = StudentVisit.objects.all().values_list('student_name', 'visit_time', 'purpose')
    for visit in visits:
        writer.writerow(visit)

    return response