from inspect import signature
from django.db.models.aggregates import Count
from django.shortcuts import render,redirect,reverse
from pytz import timezone
import datetime
from sms.models import (Categories, Courses
                        )

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
from django.contrib import messages
import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import get_template
from xhtml2pdf import pisa
import pdfkit
from django.contrib.staticfiles import finders
from quiz.models import Result, Course
from django.template import loader
from django import forms

from student.models import Payment


from django.http import JsonResponse

 

import json
from django.http import JsonResponse



from django.http import HttpResponse



from django.conf import settings
from .models import Payment

from sms.paystack import Paystack
from django.http import HttpResponse
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# from pypaystack import Transaction, Customer, Plan



def process(request):

    context = {
        'courses':'course',
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
    }

    return render(request, 'sms/dashboard/records.html', context=context)

# add to cart payment view 
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from .models import Courses, Cart, CartItem, Order, OrderItem

# end of add to ccart view
import json



import re


import requests
from django.conf import settings
from django.http import JsonResponse






from django.http import JsonResponse
from student.models import Payment, Courses
from django.shortcuts import get_object_or_404


from .forms import PDFDocumentForm

def upload_pdf_document(request):
    if request.method == 'POST':
        form = PDFDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('student:pdf_document_list')
    else:
        form = PDFDocumentForm()
    return render(request, 'student/dashboard/upload_pdf_document.html', {'form': form})


from django.shortcuts import render, redirect
from .forms import PDFDocumentForm
from .models import PDFDocument


def pdf_document_list(request):
    documents = PDFDocument.objects.all()
    return render(request, 'student/dashboard/pdf_document_list.html', {'documents': documents})


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import PDFDocument

# def pdf_document_detail(request, pk):
#     document = get_object_or_404(PDFDocument, id=pk)

#     # Check if the request is a download request
#     if request.GET.get('download'):
#         # Prepare the response with the PDF file content and set the 'Content-Disposition' header
#         response = HttpResponse(document.pdf_file, content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="{document.title}.pdf"'
#         return response
    
#     docpayment = get_object_or_404(DocPayment, id=pk)

#     context = {
#         'document':document,
#         'docpayment':docpayment,
#         'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY
#     }
#     return render(request, 'student/dashboard/pdf_document_detail.html', context=context)



def verify(request, id):

    secret_key = settings.PAYSTACK_SECRET_KEY
    api_url = f'https://api.paystack.co/transaction/verify/{id}'
    headers = {
        'Authorization': f'Bearer {secret_key}',
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
        reference = data['data']['reference']
        amount = data['data']['amount'] / 100
        email = data['data']['customer']['email']
        status = data['data']['status']
        first_name = request.user.profile.first_name
        last_name = request.user.profile.last_name

        referrer = data['data']['metadata']['referrer'].strip()
        print("Referrer URL:", referrer)

        # Split the referrer URL by '/'
        url_parts = referrer.split('/')
        print('u', url_parts)

        # Check if the last part of the URL is a numeric "id"
        if url_parts[-2].isdigit():
            id_value = url_parts[-2]
            print("Extracted ID:", id_value)
        else:
            id_value = None

        course = get_object_or_404(Courses, pk=id_value)
        print("ccc:", course)
        print('ref', reference)
        print('amoun', amount)
        print('email', email)
        print('referrer', referrer)
        print('fn', first_name)
        print('ln', last_name)

        if status == 'success':
            verified = True

            # Create the Payment object
            payment = Payment.objects.create(
                ref=reference,
                first_name=first_name,
                last_name=last_name,
                payment_user=request.user.profile,
                amount=amount,
                email=email,
                verified=verified
            )

            # Add courses to the payment using the 'set()' method
            if course:
                payment.courses.set([course])

        data = JsonResponse({'reference': reference})
    else:
        data = JsonResponse({'error': 'Payment verification failed.'}, status=400)

    print('ver', data)
    return data

from student.models import PDFDocument, DocPayment

def docverify(request, id):

    secret_key = settings.PAYSTACK_SECRET_KEY
    api_url = f'https://api.paystack.co/transaction/verify/{id}'
    headers = {
        'Authorization': f'Bearer {secret_key}',
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
        reference = data['data']['reference']
        amount = data['data']['amount'] / 100
        email = data['data']['customer']['email']
        status = data['data']['status']
        first_name = request.user.profile.first_name
        last_name = request.user.profile.last_name

        referrer = data['data']['metadata']['referrer'].strip()
        print("Referrer URL:", referrer)

        # Split the referrer URL by '/'
        url_parts = referrer.split('/')
        print('u', url_parts)

        # Check if the last part of the URL is a numeric "id"
        if url_parts[-2].isdigit():
            id_value = url_parts[-2]
            print("Extracted ID:", id_value)
        else:
            id_value = None

        course = get_object_or_404(PDFDocument, pk=id_value)
        print("ccc:", course)
        print('ref', reference)
        print('amoun', amount)
        print('email', email)
        print('referrer', referrer)
        print('fn', first_name)
        print('ln', last_name)

        if status == 'success':
            verified = True

            # Create the Payment object
            payment = DocPayment.objects.create(
                ref=reference,
                first_name=first_name,
                last_name=last_name,
                payment_user=request.user.profile,
                amount=amount,
                email=email,
                verified=verified
            )

            # Add courses to the payment using the 'set()' method
            if course:
                payment.pdfdocument.set([course])

        data = JsonResponse({'reference': reference})
    else:
        data = JsonResponse({'error': 'Payment verification failed.'}, status=400)

    print('ver', data)
    return data






# dashboard view
@login_required
def take_exams_view(request):
    course = QMODEL.Course.objects.get_queryset().order_by('id')
    context = {
        'courses':course
    }
    return render(request, 'student/dashboard/take_exams.html', context=context)

@login_required
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
    response = render(request, 'student/dashboard/start_exams.html', context=context)
    response.set_cookie('course_id', course.id)
    return response

# end of dashboard view



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

@login_required
def view_result_view(request):
    courses=QMODEL.Course.objects.get_queryset().order_by('id')
    return render(request,'student/dashboard/view_result.html',{'courses':courses})


from django.db.models import Count

@login_required
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


from django.shortcuts import render, get_object_or_404
from .models import Certificate


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


# download pdf id view
@login_required
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
    # partdesc =  get_list_or_404(QMODEL.Course, pk= pk)
    # for p in posts:
    #     print (p)
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
        # 'partdesc':partdesc,
        
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
    
