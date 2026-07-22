from django.views.generic import TemplateView
from django.shortcuts import render

class HomeView(TemplateView):
    template_name = 'home.html'

class ContactView(TemplateView):
    template_name = 'contact.html'

    def post(self, request, *args, **kwargs):
        # Handle contact form submission here
        return render(request, self.template_name, {'success': True})