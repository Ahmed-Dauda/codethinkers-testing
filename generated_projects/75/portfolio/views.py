from django.shortcuts import render
from .models import Project, Skill, Experience


def home(request):
    projects = Project.objects.all().order_by('-created_at')
    skills = Skill.objects.all().order_by('name')
    experiences = Experience.objects.all().order_by('-start_date')
    return render(request, 'list.html', {'projects': projects, 'skills': skills, 'experiences': experiences})