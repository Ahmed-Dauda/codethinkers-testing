from inspect import signature
from django.db.models.aggregates import Count
from django.shortcuts import render,redirect,reverse
from pytz import timezone
import datetime

from requests import delete
from . import models
from django.shortcuts import render, HttpResponse,redirect, get_list_or_404
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from teacher import models as TMODEL
from student.models import Logo, signature, Designcert
# from student.models import  Student
from users.models import NewUser
from users.models import Profile
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Subquery, OuterRef
#  xhtml2 pdf

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import pdfkit
from django.contrib.staticfiles import finders
from quiz.models import Result, Course
from django.template import loader

# dashboard view

def take_exams_view(request):
    course = QMODEL.Course.objects.get_queryset().order_by('id')
    context = {
        'courses':course
    }
    return render(request, 'student/dashboard/take_exams.html', context=context)

# end of dashboard view

def start_exams_view(request, pk):

    course = QMODEL.Course.objects.get(id = pk)

    # questions = QMODEL.Question.objects.all().filter(course = course)

    questions = QMODEL.Question.objects.get_queryset().filter(course = course).order_by('id')
    q_count = QMODEL.Question.objects.all().filter(course = course).count()
 
    paginator = Paginator(questions, 100) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'course':course,
        'questions':questions,
        'q_count':q_count,
        'page_obj':page_obj
    }
    if request.method == 'POST':
        pass
    response = render(request, 'student/start_exams.html', context=context)
    response.set_cookie('course_id', course.id)
    return response

@login_required
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.Course.objects.get(id=course_id)
        
        total_marks=0
        questions=QMODEL.Question.objects.get_queryset().filter(course=course).order_by('id')
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = Profile.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        
        result.marks=total_marks 
        result.exam=course
        result.student=student
        m = QMODEL.Result.objects.aggregate(Max('marks'))
        max_q = Result.objects.filter(student_id = OuterRef('student_id'),exam_id = OuterRef('exam_id'),).order_by('-marks').values('id')
        max_result = Result.objects.filter(id__in = Subquery(max_q[:1]), exam=course, student=student)
        score = 0
        for max_value in max_result:
            score = score + max_value.marks
            
        if total_marks > score:
            result.save()
        # if total_marks >= course.pass_mark:
        #     result.save()   
        # print('resulth', x)
        

        return HttpResponseRedirect('view_result')
    else:
        return HttpResponseRedirect('take-exam')

def view_result_view(request):
    courses=QMODEL.Course.objects.get_queryset().order_by('id')
    return render(request,'student/view_result.html',{'courses':courses})


from django.db.models import Count

def check_marks_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = Profile.objects.get_queryset().order_by('id')
 
    context = {
        'results':student,
        'course':course,
        'st':request.user,
        
    }
    return render(request,'student/check_marks.html', context)

#

# download pdf id view
def pdf_id_view(request, *args, **kwargs):

    course=QMODEL.Course.objects.all()
    student = Profile.objects.get(user_id=request.user.id)
    date = datetime.datetime.now()
    logo = Logo.objects.all() 
    sign = signature.objects.all()
    design = Designcert.objects.all()
    # m = QMODEL.Result.objects.aggregate(Max('marks'))  
    # max_q = Result.objects.filter(student_id = OuterRef('student_id'),exam_id = OuterRef('exam_id'),).order_by('-marks').values('id')
    # results = Result.objects.filter(id = Subquery(max_q[:1]), exam=course, student = student)
    # Result.objects.filter(id__in = Subquery(max_q[1:]), exam=course)
    
    pk = kwargs.get('pk')
    posts = get_list_or_404(course, pk= pk)
    # QMODEL.Result.objects.exclude(id = m).delete()
    user_profile =  Profile.objects.filter(user_id = request.user)
    template_path = 'student/certificatepdf.html'
    context = {
        'results': posts,
        'student':student,
        'date':date,
        'course':posts,
        'logo':logo,
        'sign':sign,
        'design':design,
        
        }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
    # find the template and render it.
    
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
   
   
    return response
    
