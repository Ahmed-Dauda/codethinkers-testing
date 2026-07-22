from django.shortcuts import render
from .models import Student

def home(request):
    students = Student.objects.all().order_by('-id')
    return render(request, 'list.html', {'students': students})