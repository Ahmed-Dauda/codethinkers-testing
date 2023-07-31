from asyncio import constants
from tokenize import group
from unittest import result
from django.contrib.auth import forms
from django.db import models
from django.db.models import fields
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from sms.models import (Categories, Courses, Topics, 
                        Comment, Blog, Blogcomment,Alert, Gallery,
                          FrequentlyAskQuestions, Partners, 
                          CourseFrequentlyAskQuestions, Skillyouwillgain,  
                          CourseLearnerReviews, 
                          Whatyouwilllearn,
                          CareerOpportunities, Whatyouwillbuild,
                          AboutCourseOwner,
                         
                        )
 
 
from profile import Profile as NewProfile

from hitcount.utils import  get_hitcount_model
from hitcount.views import HitCountMixin

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

from sms.forms import feedbackform

from django.utils import timezone
from hitcount.views import HitCountDetailView
from django.contrib.auth import get_user_model
User = get_user_model()
# cloudinary import libraries
import cloudinary
import cloudinary.uploader
import cloudinary.api

from django.views.generic import ListView
from django.http import JsonResponse

from django.http import JsonResponse
from django.core.paginator import Paginator


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
        
        
        return context

# dashboard view

class Category(LoginRequiredMixin, ListView):
    models = Categories
    template_name = 'sms/dashboard/index.html'
    success_message = 'TestModel successfully updated!'
    count_hit = True
   
    def get_queryset(self):
        return Categories.objects.all()

class Table(LoginRequiredMixin, ListView):
    models = Categories
    template_name = 'sms/dashboard/tables.html'
    success_message = 'TestModel successfully updated!'
    count_hit = True
   
    def get_queryset(self):
        return Categories.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = User.objects.all().count()

        return context
    
from sms.forms import PaymentForm
# from student.views import verify_payment
from django.conf import settings

from student.models import Payment

# from pypaystack import Transaction

from django.http import JsonResponse

from student.views import verify
import uuid


class Paymentdesc(LoginRequiredMixin, HitCountDetailView, DetailView):
    models = Courses
    template_name = 'sms/dashboard/paymentdesc.html'
    count_hit = True
    queryset = Categories.objects.all()
    def get_queryset(self):
        return Courses.objects.all()
   
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
     
        context['coursess'] = Courses.objects.all().order_by('created')[:10] 
        context['courses_count'] = Courses.objects.filter(categories__pk=self.object.id).count()
        # context['payment_course'] = Courses.objects.filter(payment__reference = payment__reference, request.user.profile=request.user.profile)
        context['category_sta'] = Categories.objects.annotate(num_course=Count('categories'))
        course = Courses.objects.get(pk=self.kwargs["pk"])

        context['course'] = Courses.objects.get(pk=self.kwargs["pk"])
        num_students = 'course.student.count()'
        context['num_students'] = num_students
        prerequisites = course.prerequisites.all()
        context['prerequisites'] = prerequisites
        context['related_courses'] = Courses.objects.filter(categories=course.categories).exclude(id=self.object.id)
        courses = Courses.objects.get(pk=self.kwargs["pk"])
        context['topics'] = Topics.objects.get_queryset().filter(courses_id=course).order_by('id')
        user = self.request.user.profile
        courses = Courses.objects.get(pk=self.kwargs["pk"])
        # Query the Payment model to get all payments related to the user and course
        related_payments = Payment.objects.filter(payment_user=user, courses=course)

        context['related_payments'] = related_payments

        context['paystack_public_key']  = settings.PAYSTACK_PUBLIC_KEY
        # Get the number of student enrollments for this user and course
        enrollment_count = related_payments.count()

        # Print or use the enrollment_count as needed
        context['enrollment_count'] = enrollment_count + 100
        print(enrollment_count)
        
        
        return context
    
class PaymentSucess(LoginRequiredMixin, HitCountDetailView, DetailView):
    models = Courses
    template_name = 'sms/dashboard/paymentsuccess.html'
    count_hit = True
    queryset = Categories.objects.all()
    def get_queryset(self):
        return Courses.objects.all()
   
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
     
        context['coursess'] = Courses.objects.all().order_by('created')[:10] 
        context['courses_count'] = Courses.objects.filter(categories__pk=self.object.id).count()
        # context['payment_course'] = Courses.objects.filter(payment__reference = payment__reference, request.user.profile=request.user.profile)
        context['category_sta'] = Categories.objects.annotate(num_course=Count('categories'))
        course = Courses.objects.get(pk=self.kwargs["pk"])

        context['course'] = Courses.objects.get(pk=self.kwargs["pk"])
        num_students = 'course.student.count()'
        context['num_students'] = num_students
        prerequisites = course.prerequisites.all()
        context['prerequisites'] = prerequisites
        context['related_courses'] = Courses.objects.filter(categories=course.categories).exclude(id=self.object.id)
        courses = Courses.objects.get(pk=self.kwargs["pk"])
        context['topics'] = Topics.objects.get_queryset().filter(courses_id=course).order_by('id')
        user = self.request.user.profile
        courses = Courses.objects.get(pk=self.kwargs["pk"])
        # Query the Payment model to get all payments related to the user and course
        related_payments = Payment.objects.filter(payment_user=user, courses=course)

        context['related_payments'] = related_payments

        context['paystack_public_key']  = settings.PAYSTACK_PUBLIC_KEY
        # Get the number of student enrollments for this user and course
        enrollment_count = related_payments.count()

        # Print or use the enrollment_count as needed
        context['enrollment_count'] = enrollment_count + 100
        print(enrollment_count)
        
        
        return context
    
from student.models import PDFDocument

class Homepage1(ListView):

    template_name = 'sms/dashboard/homepage1.html'
    success_message = 'TestModel successfully updated!'
    count_hit = True
   
    def get_queryset(self):
       
        # return  Courses.objects.all().select_related('categories').distinct()
        return  Courses.objects.all()
    
    def get_context_data(self, **kwargs): 
        context = super(Homepage1, self).get_context_data(**kwargs)
        
        context['students'] = User.objects.all().count() + 200
        context['category'] = Categories.objects.count()
        context['coursecategory'] = Categories.objects.all()
        context['courses'] = Courses.objects.all().count()
        context['gallery'] = Gallery.objects.all()
        context['blogs'] =Blog.objects.all().order_by('created')[:3]
        context['blogs_count'] =Blog.objects.all().count() 
        context['faqs'] = FrequentlyAskQuestions.objects.all()
        context['partners'] = Partners.objects.all()
        context['coursess'] = Courses.objects.all().order_by('created')[:10] 
        context['category_sta'] = Categories.objects.annotate(num_courses=Count('categories'))
        # context['newprofile'] = NewProfile.objects.all()
        context['beginner'] = Courses.objects.filter(categories__name = "BEGINNER")
        context['beginner_count'] = Courses.objects.filter(categories__name = "BEGINNER").count()

        context['intermediate'] = Courses.objects.filter(categories__name = "INTERMEDIATE")
        context['intermediate_count'] = Courses.objects.filter(categories__name = "INTERMEDIATE").count()

        context['advanced'] = Courses.objects.filter(categories__name = "ADVANCED")
        context['advanced_count'] = Courses.objects.filter(categories__name = "ADVANCED").count()


        context['Free_courses'] = Courses.objects.filter(status_type = 'Free')
        context['Free_courses_count'] = Courses.objects.filter(status_type = 'Free').count()

      
        context['latest_course'] =   Courses.objects.all().order_by('-created')[:5] 
        context['latest_course_count'] =   Courses.objects.all().order_by('-created')[:5].count()

        context['popular_course'] =   Courses.objects.all().order_by('-hit_count_generic__hits')[:3] 
    
   
        context['alert_homes']  = PDFDocument.objects.order_by('-created')[:4] 
        context['alerts']  = PDFDocument.objects.order_by('-created')
        context['alert_count_homes'] = PDFDocument.objects.order_by('-created')[:4].count() 
        context['alert_count'] = PDFDocument.objects.all().count()
        
        # context['alerts'] = Alert.objects.order_by('-created')
        # context['alert_count'] = Alert.objects.all().count()
        # context['alert_homes'] = Alert.objects.order_by('-created')[:4] 
        # context['alert_count_homes'] = Alert.objects.order_by('-created')[:4].count() 
       
        context['user'] = NewUser.objects.get_queryset().order_by('id')
        context['paystack_public_key']  = settings.PAYSTACK_PUBLIC_KEY
        
        return context


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from student.models import PDFDocument

# def pdf_document_detail(request, document_id):
#     document = get_object_or_404(PDFDocument, id=document_id)

#     # Check if the request is a download request
#     if request.GET.get('download'):
#         # Prepare the response with the PDF file content and set the 'Content-Disposition' header
#         response = HttpResponse(document.pdf_file, content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="{document.title}.pdf"'
#         return response
    
#     context = {
#         'document':document,
#         'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY
#     }
#     return render(request, 'student/dashboard/pdf_document_detail.html', context=context)


from django.contrib.messages.views import SuccessMessageMixin

class Homepage2(SuccessMessageMixin, LoginRequiredMixin,ListView):

    template_name = 'sms/dashboard/homepage2.html'
    success_message = "%(username)s was created successfully"
    count_hit = True
    
    def get_queryset(self):
       
        return  Courses.objects.all().select_related('categories').distinct()
    
    def get_context_data(self, **kwargs): 
        context = super(Homepage2, self).get_context_data(**kwargs)
        
        context['students'] = User.objects.all().count() + 100
        context['category'] = Categories.objects.count()
        context['coursecategory'] = Categories.objects.all()
        context['courses'] = Courses.objects.all().count()
        context['gallery'] = Gallery.objects.all()
        context['blogs'] =Blog.objects.all().order_by('created')[:3]
        context['blogs_count'] =Blog.objects.all().count() 
        context['user_message'] = self.request.user
        context['coursess'] = Courses.objects.all().order_by('created')[:10]
        
        context['beginner'] = Courses.objects.filter(categories__name = "BEGINNER")
        context['beginner_count'] = Courses.objects.filter(categories__name = "BEGINNER").count()

        context['intermediate'] = Courses.objects.filter(categories__name = "INTERMEDIATE")
        context['intermediate_count'] = Courses.objects.filter(categories__name = "INTERMEDIATE").count()

        context['advanced'] = Courses.objects.filter(categories__name = "ADVANCED")
        context['advanced_count'] = Courses.objects.filter(categories__name = "ADVANCED").count()

        context['Free_courses'] = Courses.objects.filter(status_type = 'Free')
        context['Free_courses_count'] = Courses.objects.filter(status_type = 'Free').count()

      
        context['latest_course'] =   Courses.objects.all().order_by('-created')[:8] 
        context['latest_course_count'] =   Courses.objects.all().order_by('-created')[:8].count()
        context['popular_course'] =   Courses.objects.all().order_by('-hit_count_generic__hits')[:3] 
    

        context['alerts'] = Alert.objects.order_by('-created')
        context['alert_count'] = Alert.objects.all().count()
        context['user'] = NewUser.objects.get_queryset().order_by('id')
        
        return context
    

class PhotoGallery(ListView):
    models = Categories
    template_name = 'sms/dashboard/homepage1.html'
    success_message = 'TestModel successfully updated!'
    count_hit = True
   
    def get_queryset(self):
        return Categories.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['c1'] = Courses.objects.filter(categories__pk = 1)
        context['students'] = User.objects.all().count()
        context['category'] = Categories.objects.count()
        context['courses'] = Courses.objects.all().count()
       
        context['coursess'] = Courses.objects.all()
        context['alerts'] = Alert.objects.order_by('-created')
        context['alert_count'] = Alert.objects.all().count()
        context['user'] = NewUser.objects.get_queryset().order_by('id')
        
        return context



from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('/')
    
class Courseslistview(LoginRequiredMixin, HitCountDetailView, DetailView):
    models = Categories
    template_name = 'sms/dashboard/courseslistview.html'
    count_hit = True
    queryset = Categories.objects.all()
    def get_queryset(self):
        return Categories.objects.all()
   
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['courses'] = Courses.objects.filter(categories__pk = self.object.id)
        context['courses_count'] = Courses.objects.filter(categories__pk = self.object.id).count()

        return context


class Bloglistview(ListView):

    models = Blog
    template_name = 'sms/dashboard/bloglistview.html'
    success_message = 'TestModel successfully updated!'
    count_hit = True
    queryset = Blog.objects.order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs_count'] =Blog.objects.all().count() 
        return context

# admin result view

class Admin_result(LoginRequiredMixin, ListView):
    models = QMODEL.Course
    template_name = 'sms/dashboard/admin_result.html'
    success_message = 'TestModel successfully updated!'
    count_hit = True
   
    def get_queryset(self):
        return QMODEL.Course.objects.all()

from student.models import Certificate

def verify_cert(request):
    certificate = get_object_or_404(Certificate, user=request.user)
    # Perform any additional verification logic here

    context = {
        'certificate': certificate,
    }
    return render(request, 'student/verify_certificate.html', context)

def verify_certificate(request, certificate_code):
    certificate = get_object_or_404(Certificate, code=certificate_code, user=request.user)
    # Perform any additional verification logic here

    context = {
        'certificate': certificate,
    }
    return render(request, 'student/verify_certificate.html', context)


@login_required
def Certificates(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    courses = QMODEL.Course.objects.all()
    cert_note = QMODEL.Certificate_note.objects.all()

    certificate = get_object_or_404(Certificate, code=pk, user=request.user)

    student = Profile.objects.get(user_id=request.user.id)
    # student = request.user.id  
    # m = QMODEL.Result.objects.aggregate(Max('marks'))  
    max_q = Result.objects.filter(student_id = OuterRef('student_id'),exam_id = OuterRef('exam_id'),).order_by('-marks').values('id')
    results = Result.objects.filter(exam=course, student = student).order_by('-date')[:1]
    Result.objects.filter(id__in = Subquery(max_q[1:]), exam=course)

    # QMODEL.Result.objects.exclude(id = m).delete()
    user_profile =  Profile.objects.filter(user_id = request.user.id)

    # results=QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    
    context = {
        'results':results,
        'course':course,
        'st':request.user,
        'user_profile':user_profile,
        'courses':courses,
        'cert_note':cert_note,
   
        # 'message': message,
    }

    
    return render(request,"sms/dashboard/certificates.html", context)


class Certdetaillistview(HitCountDetailView,DetailView):
    models = QMODEL.Course
    template_name = 'sms/dashboard/certificates.html'
    success_message = 'TestModel successfully updated!'
    count_hit = True
     
    def get_queryset(self):
        return QMODEL.Course.objects.all()

    def get_context_data(self,*args , **kwargs ):
        context = super().get_context_data(**kwargs)
        zcourse = get_object_or_404(QMODEL.Course, pk=self.kwargs['pk'])
        # course=QMODEL.Course.objects.get(id=pk)
        
        courses = QMODEL.Course.objects.all()
        cert_note = QMODEL.Certificate_note.objects.all()
        
        try:
            student = Profile.objects.get(user_id=self.request.user.id) 
        except Profile.DoesNotExist:
            return HttpResponseRedirect("account_login")
      
        max_q = Result.objects.filter(student_id = OuterRef('student_id'),exam_id = OuterRef('exam_id'),).order_by('-marks').values('id')
        results = Result.objects.filter(exam=zcourse, student = student).order_by('-date')[:1]
        Result.objects.filter(id__in = Subquery(max_q[1:]), exam=zcourse)

        try:
            user_profile =  Profile.objects.filter(user_id = self.request.user) 
        except Profile.DoesNotExist:
            return HttpResponseRedirect("account_login")
        
        # context['certificate'] = get_object_or_404(Certificate, code=self.kwargs['pk'], user=self.request.user)
        context['results'] = results
        context['course'] = zcourse
        context['st'] = self.request.user
        context['user_profile'] = user_profile
        context['courses'] = courses
        context['cert_note'] = cert_note
        
        user = self.request.user.profile
        courses = Courses.objects.get(pk=self.kwargs["pk"])
        # Query the Payment model to get all payments related to the user and course
        related_payments = Payment.objects.filter(payment_user=user, courses=courses)
        print('sta', zcourse.course_name.status_type)

        context['related_payments'] = related_payments
        context['paystack_public_key']  = settings.PAYSTACK_PUBLIC_KEY

        

        return context


class Docdetaillistview(HitCountDetailView,DetailView):
    models = PDFDocument
    template_name = 'sms/dashboard/document.html'
    success_message = 'TestModel successfully updated!'
    count_hit = True
     
    def get_queryset(self):
        return PDFDocument.objects.all()

    def get_context_data(self,*args , **kwargs ):
        context = super().get_context_data(**kwargs)
        c = get_object_or_404(PDFDocument, pk=self.kwargs['pk'])
        

        context['c'] = c
        context['paystack_public_key']  = settings.PAYSTACK_PUBLIC_KEY

        
        return context



from sms.forms import BlogcommentForm

class Blogdetaillistview(HitCountDetailView,DetailView):
    models = Blog
    template_name = 'sms/dashboard/bloglistdetailview.html'
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
# end dashboard view

   

class Courseslistdescview(LoginRequiredMixin, HitCountDetailView, DetailView):
    models = Courses
    template_name = 'sms/dashboard/courselistdesc.html'
    count_hit = True
    queryset = Categories.objects.all()
    def get_queryset(self):
        return Courses.objects.all()
   
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
      
        context['coursess'] = Courses.objects.all().order_by('created')[:10] 
        context['courses_count'] = Courses.objects.filter(categories__pk = self.object.id).count()
        context['category_sta'] = Categories.objects.annotate(num_course=Count('categories'))
        course = Courses.objects.get(pk=self.kwargs["pk"])
       
        # context['course'] = Courses.objects.get(pk=self.kwargs["pk"])
        context['course'] = Courses.objects.get(pk=self.kwargs["pk"])
    
        # print('nnnnnnnn', num_students)
        prerequisites = course.prerequisites.all()
        context['prerequisites'] = prerequisites
         # Retrieve related courses based on categorie
        context['related_courses'] = Courses.objects.filter(categories=course.categories).exclude(id=self.object.id)
      
    
        context['faqs'] = CourseFrequentlyAskQuestions.objects.all().filter(courses_id= course).order_by('id')
        context['courseLearnerReviews'] = CourseLearnerReviews.objects.filter(courses_review_id = course).order_by('id')
        context['skillyouwillgain'] = Skillyouwillgain.objects.all().filter(courses_id= course).order_by('id')
        context['whatyouwilllearn'] =   Whatyouwilllearn.objects.all().filter(courses_id= course).order_by('id')
        context['whatyouwillbuild'] =   Whatyouwillbuild.objects.all().filter(courses_id= course).order_by('id')
        context['careeropportunities'] =  CareerOpportunities.objects.all().filter(courses_id= course).order_by('id')
        context['aboutcourseowners'] =  AboutCourseOwner.objects.all().filter(courses_id= course).order_by('id')
        
        context['topics'] = Topics.objects.get_queryset().filter(courses_id= course).order_by('id')
        context['payments'] = Payment.objects.filter(courses=course).order_by('id')
    
        user = self.request.user.profile
        
        # Query the Payment model to get all payments related to the user and course
        related_payments = Payment.objects.filter(payment_user=user, courses=course)

        context['related_payments'] = related_payments
        
        enrollment_count = related_payments.count()

        # Print or use the enrollment_count as needed
        context['enrollment_count'] = enrollment_count + 100
        print(enrollment_count)
        
        return context


# new pagination

class AllKeywordsView(ListView):
    paginate_by = 1
    model = Courses
    ordering = ['created']
    template_name = "sms/blog_post_list.html"

class KeywordListView(ListView):
    paginate_by = 1
    model = Courses
    ordering = ['created']
    template_name = 'sms/blog_post_list.html'

from django.core.paginator import Paginator
from django.shortcuts import render
# ...
def listing(request, page):
    keywords = Courses.objects.all().order_by("created")
    paginator = Paginator(keywords, per_page=2)
    page_object = paginator.get_page(page)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page)
    
    context = {"page_obj": page_object}
    return render(request, "sms/blog_post_list.html", context)


def listing_api(request):
    page_number = request.GET.get("page", 1)
    per_page = request.GET.get("per_page", 2)
    startswith = request.GET.get("startswith", "")
    keywords = Courses.objects.filter(
        title__startswith=startswith
    )
    paginator = Paginator(keywords, per_page)
    page_obj = paginator.get_page(page_number)
    data = [
        {
         'title':kw.title,
         'desc':kw.desc,
         'course_desc':kw.course_desc,
         'course_link':kw.course_link,
         'created':kw.created,
         'updated':kw.updated,
        #  'hit_count_generic':kw.hit_count_generic,
        
         
         } for kw in page_obj.object_list]
    

    payload = {
        "page": {
            "current": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
        },
        "data": data
    
    }
    return JsonResponse(payload)



from student.models import PDFDocument

from django.views.generic import DetailView

class Topicslistview(LoginRequiredMixin, HitCountDetailView, DetailView):
    model = Courses
    template_name = 'sms/dashboard/topicslistviewtest1.html'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        topics = Topics.objects.filter(courses=course).order_by('id')

        transcript = []
        for topic in topics:
            if topic.transcript:
                transcript_lines = topic.transcript.split('\n')
                for line in transcript_lines:
                    line = line.strip()
                    if '|' in line:
                        time, text = line.split('|', 1)
                        transcript.append({'time': time, 'text': text.strip()})
                    else:
                        transcript.append({'time': '', 'text': line})

        context['topics'] = topics
        context['c'] = topics.count()
        context['transcript'] = transcript
        # context['alerts'] = Alert.objects.order_by('-created')
        context['alert_count'] = Alert.objects.all().count()
        context['alerts']  = PDFDocument.objects.order_by('-created')

        return context



# class Topicslistview(LoginRequiredMixin, HitCountDetailView, DetailView, ):
    
#     models = Courses
#     template_name = 'sms/dashboard/topicslistviewtest1.html'
#     count_hit = True
#     paginate_by = 1

#     def get_queryset(self):
#         return Courses.objects.get_queryset().order_by('id')
  
        
#     def get_context_data(self, **kwargs):
        
#         context = super().get_context_data(**kwargs)
#         topic = Topics.objects.get_queryset().filter(courses__pk = self.object.id).order_by('id')
#         c = Topics.objects.filter(courses__pk = self.object.id).count()
#         paginator = Paginator(topic, 1) # Show 25 contacts per page.

#         page_number = self.request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#         context['page_obj'] = page_obj
#         context['topics'] = topic
#         context['c'] = c

#         context['alerts'] = Alert.objects.order_by('-created')
#         context['alert_count'] = Alert.objects.all().count()

#         return context


class UserProfilelistview(LoginRequiredMixin, ListView):
    models = Profile
    template_name = 'sms/dashboard/myprofile.html'
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
# end



# class Topicsdetailview(LoginRequiredMixin, HitCountDetailView,DetailView):
    
#     models = Topics
#     template_name = 'sms/topicsdetailviewtest.html'
#     count_hit = True
    
#     def get_queryset(self):
#         return Topics.objects.get_queryset().order_by('id')
    
#     def get_context_data(self, **kwargs):
        
#         context = super().get_context_data(**kwargs)
#         topic = Topics.objects.get_queryset().filter(courses__pk = self.object.id).order_by('id')
#         c = Topics.objects.filter(courses__pk = self.object.id).count()
#         paginator = Paginator(topic, 1) # Show 25 contacts per page.

#         page_number = self.request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#         context['topics'] = page_obj
#         context['c'] = c

#         return context


from sweetify.views import SweetifySuccessMixin


class Commentlistview(ListView):
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
   
        
class Feedbackformview(LoginRequiredMixin,CreateView):
    
    form_class = feedbackform
    template_name =  'sms/feedbackformview.html'
    success_url = reverse_lazy('sms:feedbackformview')
   


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


@login_required
def Admin_detail_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = Profile.objects.get(user_id=request.user.id)

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
    return render(request,'sms/dashboard/admin_details.html', context)


    

    
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

# alert view
class AlertView(ListView):
    models = Alert
    template_name = 'sms/dashboard/base.html'
 
    def get_queryset(self):
        return Alert.objects.order_by('-created')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['alerts'] = Alert.objects.order_by('-created')
        context['alert_count'] = Alert.objects.all().count() 
       
        return context 

