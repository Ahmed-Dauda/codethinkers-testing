from django.shortcuts import render, redirect
from .models import Student, Class, Teacher
from django.core.paginator import Paginator

def home(request):
    students = Student.objects.all().order_by('-id')
    paginator = Paginator(students, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'list.html', {'objects': page_obj})