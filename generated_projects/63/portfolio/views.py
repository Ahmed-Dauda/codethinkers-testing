from django.shortcuts import render, redirect
from .models import Project, Skill, Experience
from .forms import ContactForm


def home(request):
    projects = Project.objects.all().order_by('-id')
    skills = Skill.objects.all().order_by('-id')
    experiences = Experience.objects.all().order_by('-id')
    return render(request, 'portfolio/list.html', {'projects': projects, 'skills': skills, 'experiences': experiences})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('portfolio:home')
    else:
        form = ContactForm()
    return render(request, 'portfolio/contact.html', {'form': form})