from django.shortcuts import render, redirect
from .models import Patient
from .forms import PatientForm

def home(request):
    patients = Patient.objects.all().order_by('-id')
    return render(request, 'list.html', {'patients': patients})

def patient_detail(request, pk):
    patient = Patient.objects.get(pk=pk)
    return render(request, 'hospital/detail.html', {'patient': patient})

def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hospital:home')
    else:
        form = PatientForm()
    return render(request, 'hospital/form.html', {'form': form})

def patient_update(request, pk):
    patient = Patient.objects.get(pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('hospital:home')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'hospital/form.html', {'form': form})