from django.shortcuts import render, redirect
from .models import Student
from .forms import ContactForm, StudentForm

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Here you would send an email or process the form
            return redirect('student_records:home')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def register_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_records:home')
    else:
        form = StudentForm()
    return render(request, 'register_student.html', {'form': form})

def dashboard(request):
    total_students = Student.objects.count()
    return render(request, 'dashboard.html', {'total_students': total_students})