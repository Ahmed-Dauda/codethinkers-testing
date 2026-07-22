from django.shortcuts import render, redirect
from .models import Student
from .forms import ContactForm, StudentForm

# Home view
def home(request):
    total_students = Student.objects.count()
    return render(request, 'home.html', {'total_students': total_students})

# About view
def about(request):
    return render(request, 'about.html')

# Contact view
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process form data
            return redirect('student_records:home')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

# Student registration view
def register_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_records:home')
    else:
        form = StudentForm()
    return render(request, 'register_student.html', {'form': form})