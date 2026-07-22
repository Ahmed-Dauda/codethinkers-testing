from django.views.generic import ListView, TemplateView, CreateView
from .models import Hero, AboutMe, Skill, Project, Experience, ContactFormSubmission
from .forms import ContactFormSubmissionForm

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hero'] = Hero.objects.first()
        context['about'] = AboutMe.objects.first()
        context['skills'] = Skill.objects.all()
        context['projects'] = Project.objects.all()
        context['experience'] = Experience.objects.all()
        return context

class AboutView(TemplateView):
    template_name = 'about.html'

class SkillsView(ListView):
    model = Skill
    template_name = 'skills.html'
    paginate_by = 25

class ProjectsView(ListView):
    model = Project
    template_name = 'projects.html'
    paginate_by = 25

class ExperienceView(ListView):
    model = Experience
    template_name = 'experience.html'
    paginate_by = 25

class ResumeView(TemplateView):
    template_name = 'resume.html'

class ContactView(CreateView):
    model = ContactFormSubmission
    form_class = ContactFormSubmissionForm
    template_name = 'contact.html'
    success_url = '/'