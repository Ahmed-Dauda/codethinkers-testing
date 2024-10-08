from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.template import loader
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db import transaction
from django.db.models import Max, Subquery, OuterRef, Count
from django.contrib import messages
from django.conf import settings
from django.db import transaction
from django.http import HttpResponseRedirect
import json
from student.models import Signature
from datetime import datetime
from django.http import JsonResponse, HttpResponseForbidden
from .models import Payment, Profile, CertificatePayment, EbooksPayment
from .models import Certificate
from pytz import timezone
# from inspect import signature
from datetime import datetime
from requests import delete
from datetime import date, timedelta
from sms.models import Categories, Courses
from student.models import PDFDocument, DocPayment
from sms.paystack import Paystack
from .models import Payment, Profile, CertificatePayment, EbooksPayment
from quiz import models as QMODEL
from teacher import models as TMODEL
from users.models import NewUser, Profile
from student.models import Logo, Designcert
from quiz.models import Result, Course
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from io import BytesIO
from pdf2image import convert_from_path
from PIL import Image
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import get_object_or_404
from .models import Course, Profile, Logo, Signature, Designcert, Certificate, NewUser
import uuid
from datetime import datetime
from django.urls import reverse

import tempfile
from io import BytesIO
from pdf2image import convert_from_path
from PIL import Image
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import get_object_or_404
from .models import Course, Profile, Logo, Signature, Designcert, Certificate, NewUser
import uuid
from datetime import datetime
from django.urls import reverse


# from pypaystack import Transaction, Customer, Plan



@csrf_exempt
@require_POST
@transaction.non_atomic_requests(using='db_name')
def paystack_webhook(request):
    # Ensure this is a POST request
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=400)

    # Parse the JSON payload from the request
    try:
        payload = json.loads(request.body)
        print("payloadttt:", payload)
    except json.JSONDecodeError as e:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON payload'}, status=400)

    # Extract relevant information from the payload
    event = payload.get('event')
    data = payload.get('data')

    # Check the event type
    if event == 'charge.success':
        # Extract information from the data
        verified = True
        reference = data.get('reference')
        paid_amount = data.get('amount') / 100
        first_name = data['customer'].get('first_name')
        last_name = data['customer'].get('last_name')
        email = data['customer'].get('email')

        referrer = payload['data']['metadata']['referrer'].strip()
        print("Referrer URL:", referrer)
        print("amount:", paid_amount)

        # Split the referrer URL by '/'
        url_parts = referrer.split('/')
        content_type = url_parts[-3]
        print("content_type", content_type)
        print('url:', url_parts[-3])
        # retrieving referral codes
        recode = get_object_or_404(NewUser, email = email)
        recode = recode.phone_number
    
        # Check if the last part of the URL is a numeric "id"
        if url_parts[-2].isdigit():
            id_value = url_parts[-2]
            print("Extracted ID:", id_value)
        else:
            id_value = None
        # print("course printed:", course)
        # course_amount = course.price
        if content_type == 'course':
            # Assuming id_value is the primary key of the Courses model
            course = get_object_or_404(Courses, pk=id_value)
            # Check if a Payment with the same reference already exists
            # user_newuser = get_object_or_404(NewUser, email=request.user)
            # print("user_newuser", user_newuser)
            # user = Profile.objects.get(id=course.id)

            # profile = get_object_or_404(Profile, id=user_id)
     
            existing_payment = Payment.objects.filter(ref=reference, email=email,amount=paid_amount,content_type=course).first()

            if not existing_payment:
                # Create a new Payment only if no existing payment is found
                payment = Payment.objects.create(
                    ref=reference,
                    amount=paid_amount,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    verified=verified,
                    content_type=course,
                    f_code=recode,
                    # payment_user=user,   
                )

                # Set courses for the Payment instance
                # course = get_object_or_404(Courses, pk=id_value)
                if course:
                    payment.courses.set([course])
             
            else:
                # Handle the case where a Payment with the same reference already exists
                # You may want to log, display an error message, or take other actions
                print(f"Payment with reference {reference} already exists.")
                            
            
        # course = get_object_or_404(Courses, pk=id_value)
        elif content_type == 'certificates':
            # Assuming id_value is the primary key of the Course model
            course = get_object_or_404(Course, pk=id_value)

            # Check if a CertificatePayment with the same reference already exists
            existing_cert_payment = CertificatePayment.objects.filter(ref=reference).first()

            if not existing_cert_payment:
                # Create a new CertificatePayment only if no existing payment is found
                cert_payment = CertificatePayment.objects.create(
                    ref=reference,
                    amount=paid_amount,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    verified=verified,
                    content_type=course,
                    f_code=recode,
                )

                # Set courses for the CertificatePayment instance
                # course = get_object_or_404(Course, pk=id_value)
                if course:
                    cert_payment.courses.set([course])
            else:
                # Handle the case where a CertificatePayment with the same reference already exists
                # You may want to log, display an error message, or take other actions
                print(f"CertificatePayment with reference {reference} already exists.")

        else:

            if content_type == 'ebooks':
                course = get_object_or_404(PDFDocument, pk=id_value)

                # Check if a payment with the same reference already exists
                existing_payment = EbooksPayment.objects.filter(ref=reference).first()

                if not existing_payment:
                    # Create a new payment only if no existing payment is found
                    epayment = EbooksPayment.objects.create(
                        ref=reference,
                        amount=paid_amount,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        verified=verified,
                        content_type=course,
                        
                    )

                    if course:
                        epayment.courses.set([course])
                else:
                    # Handle the case where a payment with the same reference already exists
                    # You may want to log, display an error message, or take other actions
                    print(f"Payment with reference {reference} already exists.")


        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Unsupported event type'}, status=400)


# end 
    
# views.py


""" import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ReferrerMentor, WithdrawalRequest

# Define the process_paystack_withdrawal function
def process_paystack_withdrawal(customer_id, amount):
    # Use Paystack API to initiate withdrawal
    # Replace 'your_paystack_secret_key' with your actual Paystack secret key

    paystack_secret_key = settings.PAYSTACK_SECRET_KEY

    withdrawal_url = 'https://api.paystack.co/transfer'
    
    headers = {
        'Authorization': f'Bearer {paystack_secret_key}',
        'Content-Type': 'application/json',
    }

    payload = {
        'source': 'balance',
        'amount': int(amount) * 100,  # Paystack uses amount in kobo (multiply by 100)
        'recipient': customer_id,
    }

    response = requests.post(withdrawal_url, json=payload, headers=headers)
    return response.json()


def withdrawal_request(request):
    if request.method == 'POST':
        referrer = ReferrerMentor.objects.filter(referrer=request.user.id).first()

        if not referrer:
            messages.error(request, 'Referrer not found.')
            return redirect('sms:myprofile')

        if not referrer.can_withdraw():
            messages.error(request, 'Withdrawal request cannot be processed. Check your balance or request status.')
            return redirect('sms:myprofile')

        if not referrer.has_paystack_customer_id():
            messages.error(request, 'Withdrawal request cannot be processed. Paystack integration is not set up for this referrer.')
            return redirect('sms:myprofile')

        amount = request.POST.get('amount')

        # Create withdrawal request
        withdrawal = WithdrawalRequest.objects.create(referrer=referrer, amount=amount, status='pending')
        referrer.withdrawal_request_status = 'pending'
        referrer.save()

        # Process withdrawal using Paystack API
        paystack_response = process_paystack_withdrawal(referrer.paystack_customer_id, amount)

        if paystack_response.get('status') == 'success':
            # Payment was successful
            messages.success(request, 'Withdrawal request submitted successfully.')
        else:
            # Payment failed
            withdrawal.status = 'rejected'
            withdrawal.save()
            messages.error(request, f'Withdrawal request failed: {paystack_response.get("message")}')

        return redirect('sms:myprofile')  # Redirect to the dashboard or wherever is appropriate

    return render(request, 'student/dashboard/withdrawal_form.html')

 """
# def withdrawal_request(request):
#     if request.method == 'POST':
#         referrer = ReferrerMentor.objects.filter(referrer=request.user.id).first()

#         if referrer and referrer.can_withdraw() and referrer.has_paystack_customer_id():
#             amount = request.POST.get('amount')

#             # Create withdrawal request
#             withdrawal = WithdrawalRequest.objects.create(referrer=referrer, amount=amount, status='pending')
#             referrer.withdrawal_request_status = 'pending'
#             referrer.save()

#             # Process withdrawal using Paystack API
#             paystack_response = process_paystack_withdrawal(referrer.paystack_customer_id, amount)

#             if paystack_response.get('status') == 'success':
#                 # Payment was successful
#                 messages.success(request, 'Withdrawal request submitted successfully.')
#             else:
#                 # Payment failed
#                 withdrawal.status = 'rejected'
#                 withdrawal.save()
#                 messages.error(request, f'Withdrawal request failed: {paystack_response.get("message")}')

#         else:
#             messages.error(request, 'Withdrawal request cannot be processed. Check your balance, request status, or Paystack integration.')

#         return redirect('sms:myprofile')  # Redirect to the dashboard or wherever is appropriate

#     return render(request, 'student/dashboard/withdrawal_form.html')


# def process_paystack_withdrawal(customer_id, amount):
#     # Use Paystack API to initiate withdrawal
#     # Replace 'your_paystack_secret_key' with your actual Paystack secret key
#     paystack_secret_key = settings.PAYSTACK_PUBLIC_KEY
#     withdrawal_url = 'https://api.paystack.co/transfer'
    
#     headers = {
#         'Authorization': f'Bearer {paystack_secret_key}',
#         'Content-Type': 'application/json',
#     }

#     payload = {
#         'source': 'balance',
#         'amount': int(amount) * 100,  # Paystack uses amount in kobo (multiply by 100)
#         'recipient': customer_id,
#     }

#     response = requests.post(withdrawal_url, json=payload, headers=headers)
#     return response.json()


# def withdrawal_request(request):
#     if request.method == 'POST':
#         # Assuming there's only one ReferrerMentor per user, if not, adjust accordingly
#         referrer = ReferrerMentor.objects.filter(referrer=request.user.id).first()

#         if referrer and referrer.can_withdraw():
#             amount = request.POST.get('amount')
#             withdrawal = WithdrawalRequest.objects.create(referrer=referrer, amount=amount, status='pending')
#             referrer.withdrawal_request_status = 'pending'
#             referrer.save()
#             messages.success(request, 'Withdrawal request submitted successfully.')
#         else:
#             messages.error(request, 'Withdrawal request cannot be processed. Check your balance or request status.')

#         return redirect('sms:myprofile')  # Redirect to the dashboard or wherever is appropriate

#     return render(request, 'student/dashboard/withdrawal_form.html')



def pdf_document_list(request):
    documents = PDFDocument.objects.all()
    return render(request, 'student/dashboard/pdf_document_list.html', {'documents': documents})





# def docverify(request, id):

#     secret_key = settings.PAYSTACK_SECRET_KEY
#     api_url = f'https://api.paystack.co/transaction/verify/{id}'
#     headers = {
#         'Authorization': f'Bearer {secret_key}',
#     }

#     response = requests.get(api_url, headers=headers)

#     if response.status_code == 200:
#         data = response.json()  # Parse the JSON response
#         reference = data['data']['reference']
#         amount = data['data']['amount'] / 100
#         email = data['data']['customer']['email']
#         status = data['data']['status']
#         first_name = request.user.profile.first_name
#         last_name = request.user.profile.last_name

#         referrer = data['data']['metadata']['referrer'].strip()
#         print("Referrer URL:", referrer)

#         # Split the referrer URL by '/'
#         url_parts = referrer.split('/')
#         print('u', url_parts)

#         # Check if the last part of the URL is a numeric "id"
#         if url_parts[-2].isdigit():
#             id_value = url_parts[-2]
#             print("Extracted ID:", id_value)
#         else:
#             id_value = None

#         course = get_object_or_404(PDFDocument, pk=id_value)


#         if status == 'success':
#             verified = True

#             # Create the Payment object
#             payment = DocPayment.objects.create(
#                 ref=reference,
#                 first_name=first_name,
#                 last_name=last_name,
#                 payment_user=request.user.profile,
#                 amount=amount,
#                 email=email,
#                 verified=verified
#             )

#             # Add courses to the payment using the 'set()' method
#             if course:
#                 payment.pdfdocument.set([course])

#         data = JsonResponse({'reference': reference})
#     else:
#         data = JsonResponse({'error': 'Payment verification failed.'}, status=400)

#     print('ver', data)
#     return data



# dashboard view
@login_required
def take_exams_view(request):
    # course = Course.objects.get_queryset().order_by('id')
    course = QMODEL.Course.objects.all()
    context = {
        'courses':course
    }
    return render(request, 'student/dashboard/take_exams.html', context=context)

# @login_required
# def start_exams_view(request, pk):
    
#     course = QMODEL.Course.objects.get(id = pk)
#     questions = QMODEL.Question.objects.get_queryset().filter(course = course).order_by('id')
#     q_count = QMODEL.Question.objects.all().filter(course = course).count()
#     paginator = Paginator(questions, 100) # Show 25 contacts per page.
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'course':course,
#         'questions':questions,
#         'q_count':q_count,
#         'page_obj':page_obj
#     }
#     if request.method == 'POST':
#         pass
#     response = render(request, 'student/dashboard/start_exams.html', context=context)
#     response.set_cookie('course_id', course.id)
#     return response

from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.core.cache import cache  # Import Django's caching framework

from django.core.cache import cache
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

@login_required
def start_exams_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    questions = QMODEL.Question.objects.filter(course=course).order_by('id')
    q_count = questions.count()
    paginator = Paginator(questions, 200)  # Show 100 questions per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate quiz end time
    quiz_duration = course.duration_minutes
    quiz_start_time = timezone.now()
    quiz_end_time = quiz_start_time + timedelta(minutes=quiz_duration)
    
    # Store the quiz end time in cache
    cache.set(f'quiz_end_time_{course.id}', quiz_end_time, timeout=None)

    # Calculate remaining time until the end of the quiz
    remaining_time = quiz_end_time - timezone.now()
    remaining_seconds = max(int(remaining_time.total_seconds()), 0)

    # updating timer
    # Get the instance of your model
    # instance = course

    # if request.method == 'POST':
    #     timer_data = request.POST.get('timer_data')
    #     # Split the timer data into minutes and seconds
    #     minutes, seconds = timer_data.split(':')
        
    #     # Convert minutes and seconds to integers
    #     minutes = int(minutes)
    #     seconds = int(seconds)
        
    #     # Calculate the total duration in minutes
    #     total_minutes = minutes + seconds / 60
    #     print("total_minutes", total_minutes)
        
    #     # Update the model with the total duration
    #     instance.duration_minutes = total_minutes
    #     instance.save()
        
    #     return JsonResponse({'status': 'success'})



    context = {
        'course': course,
        'questions': questions,
        'q_count': q_count,
        'page_obj': page_obj,
        'remaining_seconds': remaining_seconds,  # Pass remaining time to template
    }

    if request.method == 'POST':
        # Handle form submission
        pass

    response = render(request, 'student/dashboard/start_exams.html', context=context)
    response.set_cookie('course_id', course.id)
    return response

# @login_required
# def start_exams_view(request, pk):
#     course = QMODEL.Course.objects.get(id=pk)
#     questions = QMODEL.Question.objects.filter(course=course).order_by('id')
#     q_count = questions.count()
#     paginator = Paginator(questions, 100)  # Show 100 questions per page.
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     # Calculate quiz end time
#     quiz_duration = course.duration_minutes  # Assuming duration_minutes is the duration of the quiz
#     quiz_start_time = timezone.now()
#     quiz_end_time = quiz_start_time + timedelta(minutes=quiz_duration)
    
#     context = {
#         'course': course,
#         'questions': questions,
#         'q_count': q_count,
#         'page_obj': page_obj,
#         'quiz_end_time': quiz_end_time,  # Pass end time to template
        
#     }

#     if request.method == 'POST':
#         # Handle form submission
#         pass

#     response = render(request, 'student/dashboard/start_exams.html', context=context)
#     response.set_cookie('course_id', course.id)
#     return response

# end of dashboard view

import json
from django.http import JsonResponse



# example 2

@login_required
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course = QMODEL.Course.objects.get(id=course_id)
        
        total_marks = 0
        questions = QMODEL.Question.objects.filter(course=course).order_by('id')
        
        if request.body:
            json_data = json.loads(request.body)
            for i, question in enumerate(questions, start=1):
                selected_ans = json_data.get(str(i))
                print("answers" + str(i), selected_ans)
                actual_answer = question.answer
                if selected_ans == actual_answer:
                    total_marks += question.marks
        
        student = Profile.objects.get(user_id=request.user.id)
        result = QMODEL.Result.objects.create(marks=total_marks, exam=course, student=student)
        
        # Redirect to the view_result URL
        return JsonResponse({'success': True, 'message': 'Marks calculated successfully.'})
    
    else:
        return JsonResponse({'success': False, 'error': 'Course ID not found.'})

# @login_required
# def calculate_marks_view(request):
#     if request.COOKIES.get('course_id') is not None:
#         course_id = request.COOKIES.get('course_id')
#         course=QMODEL.Course.objects.get(id=course_id)
        
#         total_marks=0
#         questions=QMODEL.Question.objects.get_queryset().filter(course=course).order_by('id')
#         for i in range(len(questions)):
            
#             # selected_ans = request.COOKIES.get(str(i+1))
#             selected_ans = request.POST.get(str(i+1))
#             print("answers1", selected_ans)
#             actual_answer = questions[i].answer
#             if selected_ans == actual_answer:
#                 total_marks = total_marks + questions[i].marks
#         student = Profile.objects.get(user_id=request.user.id)
#         result = QMODEL.Result()
        
#         result.marks=total_marks 
#         result.exam=course
#         result.student=student
#         # m = QMODEL.Result.objects.aggregate(Max('marks'))
#         # max_q = Result.objects.filter(student_id = OuterRef('student_id'),exam_id = OuterRef('exam_id'),).order_by('-marks').values('id')
#         # max_result = Result.objects.filter(id__in = Subquery(max_q[:1]), exam=course, student=student)
        
#         result.save()
#         # score = 0
#         # for max_value in max_result:
#         #     score = score + max_value.marks
            
#         # if total_marks > score:
            
#         return HttpResponseRedirect('view_result')
#     else:
#         return HttpResponseRedirect('take-exam')


@login_required
def view_result_view(request):
    qcourses = Course.objects.order_by('id')

    
    context = {
        'courses':qcourses
        }

    return render(request,'student/dashboard/view_result.html', context = context)


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







# download pdf id view
# @login_required
# def pdf_id_view(request, *args, **kwargs):

#     course=QMODEL.Course.objects.all()
#     student = Profile.objects.get(user_id=request.user.id)
#     date = datetime.now()
#     logo = Logo.objects.all() 
#     sign = Signature.objects.all()  # Corrected import
#     design = Designcert.objects.all()
#     pk = kwargs.get('pk')
#     posts = get_list_or_404(course, pk= pk)
#     user_profile =  Profile.objects.filter(user_id = request.user)

#     template_path = 'student/dashboard/certificatepdf.html'

#     students =QMODEL.Student.objects.all()
#     # List to store school names
#     # school_student = get_object_or_404(QMODEL.Student, user=request.user.profile)
#     # Now you can get the associated school for this student
#     user_newuser = get_object_or_404(NewUser, email=request.user)
#     # if user_newuser.school:
#     #     context['school_name'] = user_newuser.school.school_name

#     associated_school =user_newuser.school
#     # Check if there is an associated school
#     if associated_school:
#         school_name = associated_school.school_name
#         principal_name = associated_school.name
#         portfolio = associated_school.portfolio
#         school_logo = associated_school.logo
#         school_sign = associated_school.principal_signature
#         student_name = student.first_name

#         print('principal_name', principal_name)
#         print('portfolio', portfolio)
#         print('school_name',school_name)
#         print('school_logo',school_logo)
#         print('school_sign',school_sign)
#         print('student_name', student_name)
#         student
#     else:
#         print("No associated school for this student.")

 

#     context = {
#         'results': posts,
#         'student':student,
#         'date':date,
#         'course':posts,
#         'logo':logo,
#         'sign':sign,
#         'design':design,
#         # school
#         'school_name':school_name,
#         'school_logo':school_logo,
#         'school_sign':school_sign,
#         'principal_name':principal_name,
#         'portfolio':portfolio,
        
#         }
    
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)

#     # create a pdf
#     pisa_status = pisa.CreatePDF(
#        html, dest=response)
#     # if error then show some funny view
#     if pisa_status.err:
#        return HttpResponse('We had some errors <pre>' + html + '</pre>')
   
   
#     return response
from django.urls import reverse
import uuid
from django.views.generic import TemplateView





# def verify_certificate(request, code):
#     # Retrieve the certificate using the verification code
#     certificate = get_object_or_404(Certificate, code=code)
#     student = Profile.objects.get(user_id=request.user.id)
   
#     # Generate verification URL using the shorter code field
#     verification_url = request.build_absolute_uri(
#         reverse('student:verify_certificate', args=[certificate.code])
#     )

#     context = {
#         'certificate': certificate,
#         'is_valid': True,
#         'verification_url': verification_url,
#         'student':student
#     }

#     return render(request, 'student/dashboard/verify_certificate.html', context)

# def verify_certificate(request, code):
#     # Retrieve the certificate using the verification code
#     certificate = get_object_or_404(Certificate, code=code)
#     user_newuser = get_object_or_404(NewUser, email=request.user.email)
#     student = Profile.objects.get(user_id=request.user.id)
#     date = datetime.now()

#     # Retrieve course and other related data
#     course = get_object_or_404(Course, pk=certificate.course.pk)
#     logo = Logo.objects.all()
#     sign = Signature.objects.all()
#     design = Designcert.objects.all()

#     context = {
#         'results': [course],
#         'student': student,
#         'date': date,
#         'course': [course],
#         'logo': logo,
#         'sign': sign,
#         'design': design,
#         'school_name': user_newuser.school.school_name if user_newuser.school else '',
#         'school_logo': user_newuser.school.logo if user_newuser.school else '',
#         'school_sign': user_newuser.school.principal_signature if user_newuser.school else '',
#         'principal_name': user_newuser.school.name if user_newuser.school else '',
#         'portfolio': user_newuser.school.portfolio if user_newuser.school else '',
#         'verification_url': request.build_absolute_uri(reverse('student:verify_certificate', args=[certificate.code])),
#     }

#     # Render the template for the certificate
#     template_path = 'student/dashboard/verify_certificate.html'  # Replace with your actual template path
#     template = get_template(template_path)
#     html = template.render(context)

#     # Generate the PDF
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'inline; filename="certificate.pdf"'
#     pisa_status = pisa.CreatePDF(html, dest=response)
    
#     # Check for errors
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')

#     return response


# def verify_certificate(request, code):
    
#     certificate = get_object_or_404(Certificate, code=code)
#     student = Profile.objects.get(user_id=request.user.id)
   
#     # Generate URL for PDF view using the certificate's primary key
#     pdf_url = request.build_absolute_uri(
#         reverse('student:pdf_id_view', args=[certificate.pk])
#     )

#     # Debugging: print the PDF URL
#     print(f"PDF URL: {pdf_url}")

#     context = {
#         'certificate': certificate,
#         'is_valid': True,
#         'pdf_url': pdf_url,
#         'student': student
#     }

#     return render(request, 'student/dashboard/verify_certificate.html', context)

# def verify_certificate(request, code):
#     certificate = get_object_or_404(Certificate, code=code)
#     student = Profile.objects.get(user_id=request.user.id)
   
#     # Generate URL for PDF view using the certificate's primary key
#     pdf_url = request.build_absolute_uri(
#         reverse('student:pdf_id_view', args=[certificate.pk])
#     )

#     # Get all categories
#     categories = Categories.objects.all()

#     # Create a dictionary to hold courses grouped by category
#     courses_by_category = {}
#     for category in categories:
#         # List courses for each category
#         courses_by_category[category.name] = Courses.objects.filter(categories=category)

#     # Generate URL for the courses list description
    

#     context = {
#         'certificate': certificate,
#         'is_valid': True,
#         'pdf_url': pdf_url,
#         'student': student,
#         'courses_by_category': courses_by_category,
#         'date':timezone.now().date()
        
#     }

#     return render(request, 'student/dashboard/verify_certificate.html', context)



import logging
logger = logging.getLogger(__name__)


def verify_certificate(request, code):
    # Retrieve the certificate using the code
    certificate = get_object_or_404(Certificate, code=code)

     # Generate the verification link for the certificate
    verification_link = request.build_absolute_uri(
        reverse('student:verify_certificate', args=[certificate.code])
    )
    
    # Generate URL for PDF view using the certificate's primary key
    # pdf_url = request.build_absolute_uri(
    #     reverse('student:pdf_id_view', args=[certificate.code])
    # )

    # Get all categories
    categories = Categories.objects.all()

    # Create a dictionary to hold courses grouped by category
    courses_by_category = {}
    for category in categories:
        # List courses for each category
        courses_by_category[category.name] = Courses.objects.filter(categories=category)

    context = {
        'certificate': certificate,
        'verification_link':verification_link,
        'is_valid': True,
        # 'pdf_url': pdf_url,
        'courses_by_category': courses_by_category,
        'date': timezone.now().date()
    }

    return render(request, 'student/dashboard/verify_certificate.html', context)


from django.core.exceptions import MultipleObjectsReturned

# # original pdf
def pdf_id_view(request, pk):
    # Ensure the course associated with the certificate exists
    course = get_object_or_404(Course, pk=pk)
    certificate = None

    if request.user.is_authenticated:
        user_newuser, created = NewUser.objects.get_or_create(email=request.user.email)

        try:
            # Ensure a certificate for the user and course exists or create it if not
            certificate, created = Certificate.objects.get_or_create(
                user=user_newuser,
                course=course,
                defaults={
                    'verification_code': uuid.uuid4(),
                    'code': uuid.uuid4().hex[:8]  # Generate or use existing code as needed
                }
            )
        except MultipleObjectsReturned:
            # If multiple certificates are found, get the first one or handle accordingly
            certificate = Certificate.objects.filter(user=user_newuser, course=course).first()

    else:
        # Handle case for anonymous users
        try:
            certificate, created = Certificate.objects.get_or_create(
                course=course,
                defaults={
                    'verification_code': uuid.uuid4(),
                    'code': uuid.uuid4().hex[:8]  # Generate or use existing code as needed
                }
            )
        except MultipleObjectsReturned:
            # If multiple certificates are found, get the first one or handle accordingly
            certificate = Certificate.objects.filter(course=course).first()

    # Get additional data required for rendering the PDF
    student = Profile.objects.filter(user_id=request.user.id).first() if request.user.is_authenticated else None

    date = timezone.now()
    logo = Logo.objects.all()
    sign = Signature.objects.all()
    design = Designcert.objects.all()

    # Context for rendering the PDF
    context = {
        # 'student':student,
        'results': [course],
        'first_name': certificate.user.first_name if certificate.user else 'Anonymous',
        'last_name': certificate.user.last_name if certificate.user else '',
        'date': date,
        'course': [course],
        'logo': logo,
        'sign': sign,
        'design': design,
        'school_name': certificate.user.school.school_name if certificate.user and certificate.user.school else '',
        'school_logo': certificate.user.school.logo if certificate.user and certificate.user.school else '',
        'school_sign': certificate.user.school.principal_signature if certificate.user and certificate.user.school else '',
        'principal_name': certificate.user.school.name if certificate.user and certificate.user.school else '',
        'portfolio': certificate.user.school.portfolio if certificate.user and certificate.user.school else '',
        'verification_url': request.build_absolute_uri(
            reverse('student:verify_certificate', args=[certificate.code])
        ),
    }

    # Render the PDF
    template_path = 'student/dashboard/certificatepdf_testing.html'
    template = get_template(template_path)
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="certificate.pdf"'
    
    # Create PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse(f'We had some errors <pre>{html}</pre>', status=500)

    return response


# pdf
# @login_required
# def pdf_id_view(request, pk):
#     # Ensure the course associated with the certificate exists
#     course = get_object_or_404(Course, pk=pk)

#     # Ensure the NewUser exists or create it if not
#     user_newuser, created = NewUser.objects.get_or_create(email=request.user.email)

#     # Ensure a certificate for the user and course exists or create it if not
#     certificate, created = Certificate.objects.get_or_create(
#         user=user_newuser,
#         course=course,
#         defaults={
#             'verification_code': uuid.uuid4(),
#             'code': uuid.uuid4().hex[:8]  # Generate or use existing code as needed
#         }
#     )

#     # Get additional data required for rendering the PDF
#     try:
#         student = Profile.objects.get(user_id=request.user.id)
#     except Profile.DoesNotExist:
#         return HttpResponse("Student profile not found.", status=404)
    
#     date = timezone.now()
#     logo = Logo.objects.all()
#     sign = Signature.objects.all()
#     design = Designcert.objects.all()

#     # Context for rendering the PDF
#     context = {
#         'results': [course],
#         'student': student,
#         'date': date,
#         'course': [course],
#         'logo': logo,
#         'sign': sign,
#         'design': design,
#         'school_name': certificate.user.school.school_name if certificate.user.school else '',
#         'school_logo': certificate.user.school.logo if certificate.user.school else '',
#         'school_sign': certificate.user.school.principal_signature if certificate.user.school else '',
#         'principal_name': certificate.user.school.name if certificate.user.school else '',
#         'portfolio': certificate.user.school.portfolio if certificate.user.school else '',
#         'verification_url': request.build_absolute_uri(
#             reverse('student:verify_certificate', args=[certificate.code])
#         ),
#     }

#     # Render the PDF
#     template_path = 'student/dashboard/certificatepdf_testing.html'
#     template = get_template(template_path)
#     html = template.render(context)
    
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'inline; filename="certificate.pdf"'
    
#     # Create PDF
#     pisa_status = pisa.CreatePDF(html, dest=response)
    
#     if pisa_status.err:
#         return HttpResponse(f'We had some errors <pre>{html}</pre>', status=500)

#     return response


# pdf2
# @login_required
# def pdf_id_view(request, *args, **kwargs):
#     pk = kwargs.get('pk')
#     course = get_object_or_404(Course, pk=pk)
#     student = Profile.objects.get(user_id=request.user.id)
#     date = datetime.now()
#     logo = Logo.objects.all()
#     sign = Signature.objects.all()
#     design = Designcert.objects.all()

#     template_path = 'student/dashboard/certificatepdf_testing.html'

#     # Retrieve or create a certificate for the user and course
#     user_newuser = get_object_or_404(NewUser, email=request.user.email)
#     certificate = Certificate.objects.filter(user=user_newuser, course=course).first()

#     if not certificate:
#         # If no certificate exists, create one
#         certificate = Certificate.objects.create(
#             user=user_newuser,
#             course=course,
#             verification_code=uuid.uuid4(),
#             code=uuid.uuid4().hex[:8]  # Generate or use existing code as needed
#         )

#     # Generate verification URL
#     verification_url = request.build_absolute_uri(
#         reverse('student:verify_certificate', args=[certificate.code])
#     )

#     context = {
#         'results': [course],
#         'student': student,
#         'date': date,
#         'course': [course],
#         'logo': logo,
#         'sign': sign,
#         'design': design,
#         'school_name': user_newuser.school.school_name if user_newuser.school else '',
#         'school_logo': user_newuser.school.logo if user_newuser.school else '',
#         'school_sign': user_newuser.school.principal_signature if user_newuser.school else '',
#         'principal_name': user_newuser.school.name if user_newuser.school else '',
#         'portfolio': user_newuser.school.portfolio if user_newuser.school else '',
#         'verification_url': verification_url,
#     }

#     # Determine if the request is from an iframe or direct download
#     is_iframe = request.GET.get('iframe') == 'true'

#     response = HttpResponse(content_type='application/pdf')
#     if is_iframe:
#         response['Content-Disposition'] = 'inline; filename="certificate.pdf"'
#     else:
#         response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'

#     # Render the template to HTML
#     template = get_template(template_path)
#     html = template.render(context)

#     # Generate the PDF
#     pisa_status = pisa.CreatePDF(html, dest=response)
    
#     # Check for errors
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')

#     return response


# @login_required
# def pdf_id_view(request, *args, **kwargs):
#     pk = kwargs.get('pk')
#     course = get_object_or_404(Course, pk=pk)
#     student = Profile.objects.get(user_id=request.user.id)
#     print(student, 'stt')
#     date = datetime.now()
#     logo = Logo.objects.all()
#     sign = Signature.objects.all()
#     design = Designcert.objects.all()

#     template_path = 'student/dashboard/certificatepdf_testing.html'

#     # Retrieve or create a certificate for the user and course
#     user_newuser = get_object_or_404(NewUser, email=request.user.email)
#     certificate, created = Certificate.objects.get_or_create(
#         user=user_newuser,
#         course=course,
#         defaults={'verification_code': uuid.uuid4()}
#     )

#     # Generate verification URL
#     verification_url = request.build_absolute_uri(
#         reverse('student:verify_certificate', args=[certificate.code])
#     )

#     context = {
#         'results': [course],
#         'student': student,
#         'date': date,
#         'course': [course],
#         'logo': logo,
#         'sign': sign,
#         'design': design,
#         'school_name': user_newuser.school.school_name if user_newuser.school else '',
#         'school_logo': user_newuser.school.logo if user_newuser.school else '',
#         'school_sign': user_newuser.school.principal_signature if user_newuser.school else '',
#         'principal_name': user_newuser.school.name if user_newuser.school else '',
#         'portfolio': user_newuser.school.portfolio if user_newuser.school else '',
#         'verification_url': verification_url,
#     }

#     # Determine if the request is from an iframe or direct download
#     is_iframe = request.GET.get('iframe') == 'true'

#     response = HttpResponse(content_type='application/pdf')
#     if is_iframe:
#         response['Content-Disposition'] = 'inline; filename="certificate.pdf"'
#     else:
#         response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'

#     # Render the template to HTML
#     template = get_template(template_path)
#     html = template.render(context)

#     # Generate the PDF
#     pisa_status = pisa.CreatePDF(html, dest=response)
    
#     # Check for errors
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')

#     return response


# @login_required
# def pdf_id_view(request, *args, **kwargs):
#     course = Course.objects.all()
#     student = Profile.objects.get(user_id=request.user.id)
#     date = datetime.now()
#     logo = Logo.objects.all()
#     sign = Signature.objects.all()
#     design = Designcert.objects.all()
#     pk =  kwargs.get('pk')
#     posts = get_list_or_404(course, pk=pk)
#     user_profile = Profile.objects.filter(user_id=request.user)

#     template_path = 'student/dashboard/certificatepdf_testing.html'

#     # Initialize variables with default values
#     school_name = ''
#     principal_name = ''
#     portfolio = ''
#     school_logo = ''
#     school_sign = ''

#     # Now you can get the associated school for this student
#     user_newuser = get_object_or_404(NewUser, email=request.user.email)
#     associated_school = user_newuser.school

#     # Check if there is an associated school
#     if associated_school:
#         school_name = associated_school.school_name
#         principal_name = associated_school.name
#         portfolio = associated_school.portfolio
#         school_logo = associated_school.logo
#         school_sign = associated_school.principal_signature

#         # Retrieve or create a certificate for the user and course
#     certificate, created = Certificate.objects.get_or_create(
#         user=user_newuser,
#         course=posts[0],  # Assuming there's one course here
#         defaults={'verification_code': uuid.uuid4()}
#     )

#     # Generate verification URL using the shorter code field instead of verification_code
#     # Generate verification URL using the shorter code field
#     verification_url = request.build_absolute_uri(
#         reverse('student:verify_certificate', args=[certificate.code])
#     )


#     context = {
#         'results': posts,
#         'student': student,
#         'date': date,
#         'course': posts,
#         'logo': logo,
#         'sign': sign,
#         'design': design,
#         # school
#         'school_name': school_name,
#         'school_logo': school_logo,
#         'school_sign': school_sign,
#         'principal_name': principal_name,
#         'portfolio': portfolio,
#         # Verification
#         'verification_url': verification_url,
#     }

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'

#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)

#     # create a pdf
#     pisa_status = pisa.CreatePDF(html, dest=response)
    
#     # if error then show some funny view
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')

#     return response


# @login_required
# def pdf_id_view(request, *args, **kwargs):
#     course = QMODEL.Course.objects.all()
#     student = Profile.objects.get(user_id=request.user.id)
#     date = datetime.now()
#     logo = Logo.objects.all()
#     sign = Signature.objects.all()
#     design = Designcert.objects.all()
#     pk = kwargs.get('pk')
#     posts = get_list_or_404(course, pk=pk)
#     user_profile = Profile.objects.filter(user_id=request.user)

#     template_path = 'student/dashboard/certificatepdf_testing.html'

#     # students = QMODEL.Student.objects.all()

#     # Initialize variables with default values
#     school_name = ''
#     principal_name = ''
#     portfolio = ''
#     school_logo = ''
#     school_sign = ''
#     # student_name = student.first_name

#     # Now you can get the associated school for this student
#     user_newuser = get_object_or_404(NewUser, email=request.user)

#     associated_school = user_newuser.school

#     # Check if there is an associated school
#     if associated_school:
#         school_name = associated_school.school_name
#         principal_name = associated_school.name
#         portfolio = associated_school.portfolio
#         school_logo = associated_school.logo
#         school_sign = associated_school.principal_signature

#     context = {
#         'results': posts,
#         'student': student,
#         'date': date,
#         'course': posts,
#         'logo': logo,
#         'sign': sign,
#         'design': design,
#         # school
#         'school_name': school_name,
#         'school_logo': school_logo,
#         'school_sign': school_sign,
#         'principal_name': principal_name,
#         'portfolio': portfolio,
#     }

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'

#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)

#     # create a pdf
#     pisa_status = pisa.CreatePDF(html, dest=response)
    
#     # if error then show some funny view
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')

#     return response
