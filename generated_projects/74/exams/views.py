from django.shortcuts import render
from .models import Exam

def home(request):
    exams = Exam.objects.all().order_by('-id')
    return render(request, 'list.html', {'objects': exams})