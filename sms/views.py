from asyncio import constants
from tokenize import group
from unittest import result
from django.contrib.auth import forms
from django.db import models
from django.db.models import fields
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from sms.models import (Categories, Courses, Topics, 
                        Comment, Blog, Blogcomment
                        )
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from users.models import Profile
from quiz import models as QMODEL
from django.core.paginator import Paginator    
from django.db.models import Count
import numpy as np
from django.db.models import Max, Subquery, OuterRef
# from .forms import BlogcommentForm
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required
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
        context['category'] = Categories.objects.count()
        context['courses'] = Courses.objects.all().count()
        context['user'] = NewUser.objects.get_queryset().order_by('id')
        
        # num_visit = self.request.session.get('num_visit', 0)
        # self.request.session['num_visit'] = num_visit + 1
        # context['num_visit'] = num_visit
        # context['user_name'] = self.request.user
        # context['current_users'] = get_current_users()
        # context['current_users_count'] = get_current_users().count()
        # context['comment_count'] = Comment.objects.all().count() 
    
        sweetify.success(self.request, 'You successfully changed your password')
        return context



from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('/')
    
class Courseslistview(LoginRequiredMixin, HitCountDetailView, DetailView):
    models = Categories
    template_name = 'sms/courseslistview.html'
    count_hit = True
    queryset = Categories.objects.all()
    def get_queryset(self):
        return Categories.objects.all()
   
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['courses'] = Courses.objects.filter(categories__pk = self.object.id)
        context['courses_count'] = Courses.objects.filter(categories__pk = self.object.id).count()
        # course = Courses.objects.get(pk=self.kwargs["pk"])
        
        # context['topics'] = Topics.objects.get_queryset().filter(courses_id= course).order_by('id')
        # print('tttt',Topics.objects.get(slug=self.kwargs["slug"]))
        return context

class Topicslistview(LoginRequiredMixin, HitCountDetailView, DetailView, ):
    
    models = Courses
    template_name = 'sms/topicslistview.html'
    count_hit = True
    paginate_by = 1

    def get_queryset(self):
        return Courses.objects.get_queryset().order_by('id')
  
        
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        topic = Topics.objects.get_queryset().filter(courses__pk = self.object.id).order_by('id')
        c = Topics.objects.filter(courses__pk = self.object.id).count()
        paginator = Paginator(topic, 1) # Show 25 contacts per page.

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['topics'] = page_obj
        context['c'] = c

        return context

class Topicsdetailview(LoginRequiredMixin, HitCountDetailView,DetailView):
    
    models = Topics
    template_name = 'sms/topicsdetailview.html'
    count_hit = True
    
    def get_queryset(self):
        return Topics.objects.get_queryset().order_by('id')
        

from sweetify.views import SweetifySuccessMixin


class Commentlistview( ListView):
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

class Commentlistviewsuccess( ListView):
    models = Comment
    template_name = 'sms/commentlistviewsuccess.html'
    
    def get_queryset(self):
        return Comment.objects.all()
   
        
class Feedbackformview(CreateView):
    
    form_class = feedbackform
    template_name =  'sms/feedbackformview.html'
    success_url = reverse_lazy('sms:feedbackformview')
    success_message = 'TestModel successfully updated!'

class UserProfilelistview(LoginRequiredMixin, ListView):
    models = Profile
    template_name = 'sms/myprofile.html'
    count_hit = True
   
    def get_queryset(self):
        return Profile.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_pro = self.request.user
        context['user_profile'] = Profile.objects.filter(user = self.request.user)
        course=QMODEL.Course.objects.all()
        context['courses']=QMODEL.Course.objects.all()
        # course= get_object_or_404(QMODEL.Course, pk = kwargs['pk'])
        student = Profile.objects.filter(user_id=self.request.user.id)
        context['results']= QMODEL.Result.objects.order_by('-marks')
        return context


# class Certificates(LoginRequiredMixin, ListView):
#     models = Profile
#     template_name = 'sms/pdf_all.html'
#     count_hit = True
   
#     def get_queryset(self):
#         return Profile.objects.all()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user_pro = self.request.user
#         context['user_profile'] = Profile.objects.filter(user = self.request.user)
#         course=QMODEL.Course.objects.all()
#         context['courses']=QMODEL.Course.objects.all()
#         # course= get_object_or_404(QMODEL.Course, pk = kwargs['pk'])
#         student = Profile.objects.get(user_id=self.request.user.id)
#         context['results']= QMODEL.Result.objects.all().order_by('-marks')
#         return context
    

@login_required
def Certificates(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    courses = QMODEL.Course.objects.all()
    cert_note = QMODEL.Certificate_note.objects.all()
    
    # student = Profile.objects.get(user_id=request.user.id)
    student = request.user.id  
    # m = QMODEL.Result.objects.aggregate(Max('marks'))  
    max_q = Result.objects.filter(student_id = OuterRef('student_id'),exam_id = OuterRef('exam_id'),).order_by('-marks').values('id')
    results = Result.objects.filter(exam=course, student = student).order_by('-date')[:1]
    # Result.objects.filter(id__in = Subquery(max_q[1:]), exam=course)
      
    
    # QMODEL.Result.objects.exclude(id = m).delete()
    user_profile =  Profile.objects.filter(user_id = request.user)

    # results=QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
              
    context = {
        'results':results,
        'course':course,
        'st':request.user,
        'user_profile':user_profile,
        'courses':courses,
        'cert_note':cert_note
    }
    return render(request,'sms/certificates.html', context)


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
    success_url= reverse_lazy('sms:myprofile')
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


@login_required
def Admin_detail_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = Profile.objects.filter(user_id=request.user.id)

    # m = QMODEL.Result.objects.aggregate(Max('marks'))   
    # max_q = QMODEL.Result.objects.filter(student_id = OuterRef('student_id'), exam_id = OuterRef('exam_id') ,).order_by('-marks').values('id')
    max_q = Result.objects.filter(student_id = OuterRef('student_id'),exam_id = OuterRef('exam_id'),).order_by('-marks').values('id')
    results = Result.objects.filter(id = Subquery(max_q[:1]), exam=course).order_by('-marks')
    Result.objects.filter(id__in = Subquery(max_q[1:]), exam=course, marks = 1).delete()   
 
    context = { 
        'results':results,
        'course':course,
        'st':request.user,
     
    }
    return render(request,'sms/Admin_result_detail_view.html', context)

class Bloglistview(ListView):
    models = Blog
    template_name = 'sms/bloglistview.html'
    success_message = 'TestModel successfully updated!'
    count_hit = True
    queryset = Blog.objects.order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs_count'] =Blog.objects.all().count() 
        return context
    
from sms.forms import BlogcommentForm
class Blogdetaillistview(HitCountDetailView,DetailView):
    models = Blog
    template_name = 'sms/bloglistdetailview.html'
    success_message = 'TestModel successfully updated!'
    count_hit = True
     
    def get_queryset(self):
        return Blog.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['blogs'] =Blog.objects.get_queryset().order_by('id')
        comments = Blogcomment.objects.filter(post__slug=self.object.slug).order_by('-created')
        context['blogs_count'] =Blog.objects.all().count()
        context['comments'] = comments 
        context['comments_count'] = comments.count() 
       
        return context
    
class BlogcommentCreateView( CreateView):
    model = Blogcomment
    form_class= BlogcommentForm
    template_name = 'sms/blogcomment.html'
    # fields = ['id','post' ,'author','content']
    def get_success_url(self):
        return reverse_lazy('sms:blogdetaillistview', kwargs= {'slug':self.kwargs['slug']})
    
    # def form_valid(self, form):
    #     form.instance.author_id=self.request.user.id
    #     return super().form_valid(form)
    
    def form_valid(self, form):
        # form.instance.author_id=self.request.user.id
        form.instance.post = Blog.objects.get(slug=self.kwargs["slug"])
        
        return super().form_valid(form)
    
    
    # success_url = reverse_lazy("sms:bloglistview")
    # def get_context_data(self,**kwargs):
        
    #     context = super().get_context_data(**kwargs)
        # com= comment.comments.all()
        # comments_connected = Blogcomment.objects.all().order_by('-created')
        # comments_connected = Blogcomment.objects.all().order_by('-created')
        
        # context['blogs'] =Blog.objects.all() 
        # context['blogs_count'] =Blog.objects.all().count() 
        # context['comments'] = com
       
        # return context
# arbitrary view
class Baseblogview(HitCountDetailView,DetailView):
    models = Blog
    template_name = 'sms/baseblog.html'
    success_message = 'TestModel successfully updated!'
    count_hit = True

    def get_queryset(self):
        return Blog.objects.order_by('-created')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['blogs'] =Blog.objects.order_by('-created')
        context['blogs_count'] =Blog.objects.all().count() 
       
        return context
    

