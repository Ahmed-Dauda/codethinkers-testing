from tokenize import group
from unittest import result
from django.contrib.auth import forms
from django.db import models
from django.db.models import fields
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from sms.models import Categories, Courses, Topics, Comment, course_links
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from users.models import Profile
from quiz import models as QMODEL
from quiz.models import Result, Course
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

from django.utils import timezone
from hitcount.views import HitCountDetailView
from django.contrib.auth import get_user_model
User = get_user_model()
# cloudinary import libraries
import cloudinary
import cloudinary.uploader
import cloudinary.api

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
        context['course_links'] = course_links.objects.filter(courses_id = self.object.id)
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
   
        
class Feedbackformview(CreateView):
    
    form_class = feedbackform
    template_name =  'sms/feedbackformview.html'
    success_url = reverse_lazy('sms:feedbackformview')
    success_message = 'TestModel successfully updated!'

# class UserProfilelistview(LoginRequiredMixin, ListView):
#     models = Profile
#     template_name = 'sms/profile.html'
#     success_message = 'TestModel successfully updated!'
#     count_hit = True
   
#     def get_queryset(self):
#         return Profile.objects.all()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user_pro = self.request.user
#         context['user_profile'] = Profile.objects.filter(user = self.request.user)
#         course=QMODEL.Course.objects.all()
#         # course=QMODEL.Course.objects.get(id_in =course)
#         # course= get_object_or_404(QMODEL.Course, pk = kwargs['pk'])
#         student = Profile.objects.get(user_id=self.request.user.id)
#         context['results']= QMODEL.Result.objects.order_by('-marks').filter(exam=course).filter(student=student)[:3]
#         return context
from django.db.models import Count
import numpy as np
from django.db.models import Max, Subquery, OuterRef

from django.contrib.auth.decorators import login_required

@login_required
def userprofileview(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    # student = Profile.objects.get(user_id=request.user.id)
    student = request.user.id  
    # m = QMODEL.Result.objects.aggregate(Max('marks'))  
    max_q = Result.objects.filter(student_id = OuterRef('student_id'),exam_id = OuterRef('exam_id'),).order_by('-marks').values('id')
    results = Result.objects.filter(id = Subquery(max_q[:1]), exam=course, student = student)
    Result.objects.filter(id = Subquery(max_q[1:]), exam=course, marks=1).delete()
    # QMODEL.Result.objects.exclude(id = m).delete()
    user_profile =  Profile.objects.filter(user_id = request.user)

    # results=QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
              
    context = {
        'results':results,
        'course':course,
        'st':request.user,
        'user_profile':user_profile 
    }
    return render(request,'sms/profile.html', context)

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

# admin result view

class Admin_result(LoginRequiredMixin, ListView):
    models = QMODEL.Course
    template_name = 'sms/admin_result.html'
    success_message = 'TestModel successfully updated!'
    count_hit = True
   
    def get_queryset(self):
        return QMODEL.Course.objects.all()



def Admin_detail_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = Profile.objects.get(user_id=request.user.id)

    # m = QMODEL.Result.objects.aggregate(Max('marks'))   
    # max_q = QMODEL.Result.objects.filter(student_id = OuterRef('student_id'), exam_id = OuterRef('exam_id') ,).order_by('-marks').values('id')
    max_q = Result.objects.filter(student_id = OuterRef('student_id'),exam_id = OuterRef('exam_id'),).order_by('-marks').values('id')
    results = Result.objects.filter(id = Subquery(max_q[:1]), exam=course).order_by('-marks')
    Result.objects.filter(id = Subquery(max_q[1:]), exam=course).delete()   
    # max_q = QMODEL.Result.objects.filter(marks = OuterRef('marks') ,).order_by('-marks').values('id')
    # results = QMODEL.Result.objects.filter(id = Subquery(max_q[:1]), marks__gte =2)
    # QMODEL.Result.objects.exclude(id = results[:1]).delete() 
    # QMODEL.Result.objects.get(~Q(id = results[:1]), student_id = results[:1].student.id, exam_id = results[:1].exam.id).delete()

    
    context = { 
        'results':results,
        'course':course,
        'st':request.user,
        # 'm':m
    }
    return render(request,'sms/Admin_result_detail_view.html', context)

# class Admin_result_detail_view(LoginRequiredMixin, DetailView):
#     models = QMODEL.Result
#     template_name = 'sms/Admin_result_detail_view.html'
#     success_message = 'TestModel successfully updated!'
#     count_hit = True
   
#     def get_queryset(self):
#         return QMODEL.Result.objects.all()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         max_q = QMODEL.Result.objects.filter(student_id = OuterRef('student_id'), exam_id = OuterRef('exam_id'), ).order_by('-marks').values('id')
#         context['results'] = QMODEL.Result.objects.filter(id = Subquery(max_q[:1])) 
#         return context