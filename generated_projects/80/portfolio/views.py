from django.views.generic import TemplateView
from .models import Skill, Project, Experience, About

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skills'] = Skill.objects.all().order_by('-id')
        context['projects'] = Project.objects.all().order_by('-id')
        context['experiences'] = Experience.objects.all().order_by('-id')
        context['about'] = About.objects.first()  # Fetching the first About instance
        return context



class AboutView(ListView):
    model = About
    template_name = 'about.html'
    context_object_name = 'objects'
    ordering = ['-id']