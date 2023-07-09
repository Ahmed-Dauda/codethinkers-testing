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

import requests    
from django.http import JsonResponse
     





# def make_payment(request:HttpResponse) -> HttpResponse:
#     if request.method == 'POST':
#         payment_form = PaymentForm(request.POST)
#         if payment_form.is_valid():
#         # payment = payment_form.save(commit=False)
#             payment = payment_form.save()
#         # payment_status = verify_payment(payment.ref)
#         # if payment_status == 'success':
#         #     payment.verified = True
                   
#             return render(request, 'student/make_payment.html', {'payment': payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
#     # else:
#     #     payment_form = PaymentForm()
#     # return render (request, 'student/initiate_payment.html', {'payment_form':payment_form})
           
 
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
import requests


def get_payment_status(request, reference):
    url = f'https://api.paystack.co/transaction/verify/{reference}'
   
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    status = data['data']['status']
    amount_paid = data['data']['amount']

    return JsonResponse({'status': status, 'amount_paid': amount_paid})




def get_customer_references():
    url = "https://api.paystack.co/customer"

    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        customer_references = data.get('data', [])
        return customer_references
    else:
        # Handle the API request error here
        return []

from django.http import JsonResponse

def customer_references_view(request):
    customer_references = get_customer_references()
    return JsonResponse(customer_references, safe=False)


import requests
from django.shortcuts import render
from django.conf import settings
from .models import Payment

from sms.paystack import Paystack
from django.http import HttpResponse
import json

def handle_webhook(request):
    if request.method == 'POST':
        # Parse the webhook data
        payload = json.loads(request.body)
        event = payload['event']
        data = payload['data']

        # Check if the event is a successful payment
        if event == 'charge.success':
            payment_reference = data['reference']
            
            # Process the payment reference as needed
            # ...

        # Respond with a 200 OK status
        return HttpResponse(status=200)


def process_payment(request):

    if request.method == 'POST':
        ref = request.POST.get('ref')
        amount_str = request.POST.get('amount')
        amount = int(amount_str.replace(',', ''))
        email = request.POST.get('email')

          
        # Fetch payment status and amount from Paystack API
        ref = 568560343
        url = f'https://api.paystack.co/transaction/verify/{ref}'
      
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        data = response.json()

        status = data['data']['status']
        print('status', status)
        if status == 'success':
            verified = True
        amount_paid = data['data']['amount']/100
        print('amount',amount_paid)

        # Save the payment information to the database
        payment = Payment(ref=ref, amount=amount_paid, verified=verified, email=email)
        payment.save()

        # Redirect or render a success page
        return render(request, 'student/verification_result.html', {'amount': amount, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
    else:
        # Render the payment form
        return render(request, 'sms/dashboard/paymentdesc.html', {'amount': amount})

# def process_payment(request):

#     if request.method == 'POST':
#         ref = request.POST.get('ref')
#         amount_str = request.POST.get('amount')
#         amount = int(amount_str.replace(',', ''))
#         verified = request.POST.get('verified')
#         email = request.POST.get('email')
    
#         # Save the payment information to the database
#         payment = Payment(ref=ref, amount=amount, verified=verified, email=email)
#         payment.save()

#         # Redirect or render a success page
#         return render(request, 'student/verification_result.html', {'amount': amount, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
#     else:
#         # Render the payment form
#         return render (request, 'sms/dashboard/paymentdesc.html', {'amount':amount})






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
    
