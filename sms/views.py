from django.contrib.auth import forms
from django.db import models
from django.db.models import fields
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from sms.models import Categories, Courses, Topics, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from users.models import Profile
# from django.contrib.auth.models import User
from users.forms import userprofileform, SimpleSignupForm
# password reset import

from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
# from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages #import messages
# end password reset import.
from users.models import NewUser

# from sms.forms import signupform
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
import sweetify
from sms.forms import feedbackform

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sessions.models import Session
# from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from hitcount.views import HitCountDetailView
from django.contrib.auth import get_user_model
User = get_user_model()

# def get_current_users():
#     active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
#     user_id_list = []
#     for session in active_sessions:
#         data = session.get_decoded()
#         user_id_list.append(data.get('_auth_user_id', None))
#     # Query all logged in users based on id list
#     return User.objects.filter(id__in=user_id_list)



class Categorieslistview(LoginRequiredMixin, ListView):
    models = Categories
    template_name = 'sms/home.html'
    success_message = 'TestModel successfully updated!'
    count_hit = True
   
    def get_queryset(self):
        return Categories.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = User.objects.all().count()
        context['category'] = Categories.objects.all().count()
        context['courses'] = Courses.objects.all().count()
        context['user'] = NewUser.objects.all()
        # num_visit = self.request.session.get('num_visit', 0)
        # self.request.session['num_visit'] = num_visit + 1
        # context['num_visit'] = num_visit
        # context['user_name'] = self.request.user
        # context['current_users'] = get_current_users()
        # context['current_users_count'] = get_current_users().count()
        context['comment_count'] = Comment.objects.all().count() 
    
        sweetify.success(self.request, 'You successfully changed your password')
        return context



from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('/')

        
class Courseslistview( HitCountDetailView,LoginRequiredMixin, DetailView):
    models = Categories
    template_name = 'sms/courseslistview.html'
    count_hit = True
    queryset = Categories.objects.all()
    def get_queryset(self):
        return Categories.objects.all()
   
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['courses'] = Courses.objects.filter(categories__pk = self.object.id)
        context['courses_count'] = Courses.objects.filter(categories__pk = self.object.id)

        return context

class Topicslistview( HitCountDetailView,LoginRequiredMixin, DetailView, ):
    models = Courses
    template_name = 'sms/topicslistview.html'
    count_hit = True

    def get_queryset(self):
        return Courses.objects.all()
  
        
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['topics'] = Topics.objects.filter(courses__pk = self.object.id) 
        context['topics_count'] = Topics.objects.filter(courses__pk = self.object.id) 
        return context

class Topicsdetailview( HitCountDetailView,LoginRequiredMixin,DetailView):
    models = Topics
    template_name = 'sms/topicsdetailview.html'
    count_hit = True
    
    def get_queryset(self):
        return Topics.objects.all()
        

from sweetify.views import SweetifySuccessMixin

# class signupview(SuccessMessageMixin,CreateView):
    
#     form_class =signupform
#     template_name =  'sms/signup.html'
#     success_url = reverse_lazy('sms:signupsuccess')
#     success_message = 'TestModel successfully updated!'
    
# class Signupsuccess(ListView):
#     models = ''
#     template_name = 'sms/signupsuccess.html'
#     success_url = reverse_lazy('sms:signupview')

#     def get_queryset(self):
#         return Topics.objects.all()

class Commentlistview(LoginRequiredMixin, ListView):
    models = Comment
    template_name = 'sms/commentlistview.html'

    def get_queryset(self):
        return Comment.objects.all()
    
        
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all() 
        context['user_comment'] = self.request.user
        context['comment_count'] = Comment.objects.all().count() 
        return context

class Commentlistviewsuccess(LoginRequiredMixin, ListView):
    models = Comment
    template_name = 'sms/commentlistviewsuccess.html'
    
    def get_queryset(self):
        return Comment.objects.all()
   
        
class Feedbackformview(SuccessMessageMixin,CreateView):
    
    form_class = feedbackform
    template_name =  'sms/feedbackformview.html'
    success_url = reverse_lazy('sms:feedbackformview')
    success_message = 'TestModel successfully updated!'

class UserProfilelistview(LoginRequiredMixin, ListView):
    models = Profile
    template_name = 'sms/profile.html'
    success_message = 'TestModel successfully updated!'
    count_hit = True
   
    def get_queryset(self):
        return Profile.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_pro = self.request.user
        context['user_profile'] = Profile.objects.filter(user = self.request.user)
        return context

class UserProfileForm(LoginRequiredMixin, CreateView):
    models = Profile
    fields = '__all__'
    template_name = 'sms/userprofileform.html'
    success_message = 'TestModel successfully updated!'
    count_hit = True

    def get_queryset(self):
        return Profile.objects.all()

class UserProfileUpdateForm(LoginRequiredMixin, UpdateView):
    models = Profile
    fields = '__all__'
    template_name = 'sms/userprofileupdateform.html'
    success_message = 'TestModel successfully updated!'
    count_hit = True

    def get_queryset(self):
        return Profile.objects.all()