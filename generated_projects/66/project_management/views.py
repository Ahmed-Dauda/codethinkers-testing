from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Owner
from .forms import ProjectForm

def project_list(request):
    projects = Project.objects.order_by('-id')
    return render(request, 'project_management/list.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'project_management/detail.html', {'project': project})

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_management:project_list')
    else:
        form = ProjectForm()
    return render(request, 'project_management/form.html', {'form': form})

def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_management:project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project_management/form.html', {'form': form})