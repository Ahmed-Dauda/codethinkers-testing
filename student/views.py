import os
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
from instructor.models import InstructorEarning
from instructor.utils import process_certificate_payment_earnings, process_course_payment_earnings
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
import logging

# from pypaystack import Transaction, Customer, Plan
from instructor.utils import process_course_payment_earnings, process_certificate_payment_earnings

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
@transaction.non_atomic_requests(using='db_name')  # replace with your DB alias
def paystack_webhook(request):
    import json
    from django.http import JsonResponse
    from django.shortcuts import get_object_or_404

    try:
        payload = json.loads(request.body)
        print("Payload received:", payload)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)

    if payload.get('event') != 'charge.success':
        return JsonResponse({'error': 'Unsupported event'}, status=400)

    data = payload['data']
    reference = data.get('reference')
    amount = int(data.get('amount', 0) / 100)
    email = data['customer'].get('email')
    first_name = data['customer'].get('first_name')
    last_name = data['customer'].get('last_name')

    # ---- Extract content type and ID from referrer ----
    referrer = data.get('metadata', {}).get('referrer', '')
    parts = referrer.strip('/').split('/')
    if len(parts) < 2:
        return JsonResponse({'error': 'Invalid referrer'}, status=400)

    content_type = parts[-2]
    object_id = parts[-1] if parts[-1].isdigit() else None

    try:
        if content_type == 'course' and object_id:
            course = get_object_or_404(Courses, id=object_id)

            # ---- Prevent duplicate payments ----
            payment, created = Payment.objects.get_or_create(
                ref=reference,
                defaults={
                    'amount': amount,
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'verified': True,
                    'content_type': course,
                }
            )
            payment.courses.set([course])
         
            # ---- Create InstructorEarning only if we can find the instructor ----
            instructor_email = course.course_owner if hasattr(course, 'course_owner') else request.user.email
            
            instructor = NewUser.objects.filter(email=instructor_email).first()

            if instructor:
                # Prevent duplicate earnings
                if not InstructorEarning.objects.filter(payment=payment, course=course).exists():
                    commission_rate = 30
                    instructor_amount = int(amount * (100 - commission_rate) / 100)
                    platform_amount = amount - instructor_amount

                    InstructorEarning.objects.create(
                        instructor=instructor,
                        course=course,
                        payment=payment,
                        amount_paid=amount,
                        commission_rate=commission_rate,
                        instructor_amount=instructor_amount,
                        platform_amount=platform_amount,
                        is_paid_out=False
                    )
            else:
                print(f"[Webhook] Instructor not found for course {course.id} ({course.course_owner})")

        # ----- Certificates -----
        elif content_type == 'certificates' and object_id:
            cert_course = get_object_or_404(Courses, id=object_id)
            cert_payment, created = CertificatePayment.objects.get_or_create(
                ref=reference,
                defaults={
                    'amount': amount,
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'verified': True,
                    'content_type': cert_course,
                }
            )
            cert_payment.courses.set([cert_course])

            instructor_email = cert_course.course_owner
            instructor = NewUser.objects.filter(email=instructor_email).first()

            if instructor and not InstructorEarning.objects.filter(certificate_payment=cert_payment, course=cert_course).exists():
                commission_rate = 30
                instructor_amount = int(amount * (100 - commission_rate) / 100)
                platform_amount = amount - instructor_amount

                InstructorEarning.objects.create(
                    instructor=instructor,
                    course=cert_course,
                    certificate_payment=cert_payment,
                    amount_paid=amount,
                    commission_rate=commission_rate,
                    instructor_amount=instructor_amount,
                    platform_amount=platform_amount,
                    is_paid_out=False
                )

        # ----- Ebooks -----
        elif content_type == 'ebooks' and object_id:
            ebook = get_object_or_404(PDFDocument, id=object_id)
            epayment, created = EbooksPayment.objects.get_or_create(
                ref=reference,
                defaults={
                    'amount': amount,
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'verified': True,
                    'content_type': ebook,
                }
            )
            epayment.courses.set([ebook])

    except Exception as e:
        print(f"[Webhook Error] {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    print("[Webhook] Payment & InstructorEarning saved successfully")
    return JsonResponse({'status': 'success'})


# End of webhook view
# @csrf_exempt
# @require_POST
# @transaction.non_atomic_requests(using='db_name')
# def paystack_webhook(request):
#     # Ensure this is a POST request
#     if request.method != 'POST':
#         return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=400)

#     # Parse the JSON payload from the request
#     try:
#         payload = json.loads(request.body)
#         print("payloadttt:", payload)
#     except json.JSONDecodeError as e:
#         return JsonResponse({'status': 'error', 'message': 'Invalid JSON payload'}, status=400)

#     # Extract relevant information from the payload
#     event = payload.get('event')
#     data = payload.get('data')

#     # Check the event type
#     if event == 'charge.success':
#         # Extract information from the data
#         verified = True
#         reference = data.get('reference')
#         paid_amount = data.get('amount') / 100
#         first_name = data['customer'].get('first_name')
#         last_name = data['customer'].get('last_name')
#         email = data['customer'].get('email')

#         referrer = payload['data']['metadata']['referrer'].strip()
#         # print("Referrer URL:", referrer)
#         # print("amount:", paid_amount)

#         # Split the referrer URL by '/'
#         url_parts = referrer.split('/')
#         content_type = url_parts[-3]
#         # print("content_type", content_type)
#         # print('url:', url_parts[-3])
#         # retrieving referral codes
#         recode = get_object_or_404(NewUser, email = email)
#         recode = recode.phone_number
    
#         # Check if the last part of the URL is a numeric "id"
#         if url_parts[-2].isdigit():
#             id_value = url_parts[-2]
#             # print("Extracted ID:", id_value)
#         else:
#             id_value = None
#         # print("course printed:", course)
#         # course_amount = course.price
#         if content_type == 'course':
#             # Assuming id_value is the primary key of the Courses model
#             course = get_object_or_404(Courses, pk=id_value)
#             # Check if a Payment with the same reference already exists
#             # user_newuser = get_object_or_404(NewUser, email=request.user)
#             # print("user_newuser", user_newuser)
#             # user = Profile.objects.get(id=course.id)

#             # profile = get_object_or_404(Profile, id=user_id)
     
#             existing_payment = Payment.objects.filter(ref=reference, email=email,amount=paid_amount,content_type=course).first()

#             if not existing_payment:
#                 # Create a new Payment only if no existing payment is found
#                 payment = Payment.objects.create(
#                     ref=reference,
#                     amount=paid_amount,
#                     first_name=first_name,
#                     last_name=last_name,
#                     email=email,
#                     verified=verified,
#                     content_type=course,
#                     f_code=recode,
#                     # payment_user=user,   
#                 )

#                 # Set courses for the Payment instance
#                 # course = get_object_or_404(Courses, pk=id_value)
#                 if course:
#                     payment.courses.set([course])
             
#             else:
#                 # Handle the case where a Payment with the same reference already exists
#                 # You may want to log, display an error message, or take other actions
#                 print(f"Payment with reference {reference} already exists.")
                            
            
#         # course = get_object_or_404(Courses, pk=id_value)
#         elif content_type == 'certificates':
#             # Assuming id_value is the primary key of the Course model
#             course = get_object_or_404(Course, pk=id_value)

#             # Check if a CertificatePayment with the same reference already exists
#             existing_cert_payment = CertificatePayment.objects.filter(ref=reference).first()

#             if not existing_cert_payment:
#                 # Create a new CertificatePayment only if no existing payment is found
#                 cert_payment = CertificatePayment.objects.create(
#                     ref=reference,
#                     amount=paid_amount,
#                     first_name=first_name,
#                     last_name=last_name,
#                     email=email,
#                     verified=verified,
#                     content_type=course,
#                     f_code=recode,
#                 )

#                 # Set courses for the CertificatePayment instance
#                 # course = get_object_or_404(Course, pk=id_value)
#                 if course:
#                     cert_payment.courses.set([course])
#             else:
#                 # Handle the case where a CertificatePayment with the same reference already exists
#                 # You may want to log, display an error message, or take other actions
#                 print(f"CertificatePayment with reference {reference} already exists.")

#         else:

#             if content_type == 'ebooks':
#                 course = get_object_or_404(PDFDocument, pk=id_value)

#                 # Check if a payment with the same reference already exists
#                 existing_payment = EbooksPayment.objects.filter(ref=reference).first()

#                 if not existing_payment:
#                     # Create a new payment only if no existing payment is found
#                     epayment = EbooksPayment.objects.create(
#                         ref=reference,
#                         amount=paid_amount,
#                         first_name=first_name,
#                         last_name=last_name,
#                         email=email,
#                         verified=verified,
#                         content_type=course,
                        
#                     )

#                     if course:
#                         epayment.courses.set([course])
#                 else:
#                     # Handle the case where a payment with the same reference already exists
#                     # You may want to log, display an error message, or take other actions
#                     print(f"Payment with reference {reference} already exists.")


#         return JsonResponse({'status': 'success'})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Unsupported event type'}, status=400)


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




@login_required
def take_exams_view(request):
    categories = Categories.objects.prefetch_related('category').all()
    context = {
        'categories': categories
    }
    return render(request, 'student/dashboard/take_exams.html', context)

# @login_required
# def take_exams_view(request):
#     # course = Course.objects.get_queryset().order_by('id')
#     course = QMODEL.Course.objects.all()
#     context = {
#         'courses':course
#     }
#     return render(request, 'student/dashboard/take_exams.html', context=context)


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


from django.shortcuts import render, redirect
from asgiref.sync import sync_to_async, async_to_sync
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpRequest
 # replace with actual import
import random
from quiz.models import Question,StudentExamSession


@csrf_exempt
def start_exams_view(request: HttpRequest, pk: int) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('account_login')
    return async_to_sync(_start_exam_async)(request, pk)

# ---------- ASYNC VERSION ----------
async def _start_exam_async(request, pk):
    user = request.user
    user_profile = await get_user_profile(user)
    course = await get_course(pk)
    all_questions = await get_course_questions(course)
    result_exists = await check_result_exists(user_profile, course)

    # if result_exists:
    #     return await async_redirect('student:view_result')

    # Get shuffled questions from saved session or create new
    all_shuffled_questions = await get_or_create_shuffled_questions(user_profile, course, all_questions)

    # Trim to course.show_questions limit
    show_count = course.show_questions or len(all_shuffled_questions)
    questions = all_shuffled_questions[:show_count]
    q_count = len(questions)

    context = {
        'course': course,
        'questions': questions,
        'q_count': q_count,
        'page_obj': questions,
        'quiz_already_submitted': result_exists,
        'tab_limit': course.num_attemps,
    }

    response = await async_render(request, 'student/dashboard/start_exams.html', context)
    response.set_cookie('course_id', course.id)
    return response

# ---------- ASYNC HELPERS ----------
@sync_to_async
def get_user_profile(user):
    return user.profile

@sync_to_async
def get_course(pk):
    return Course.objects.select_related('course_name').only(
        'id', 'room_name', 'course_name__id', 'exam_type__name',
        'course_name__title', 'num_attemps', 'show_questions', 'duration_minutes'
    ).get(id=pk)

@sync_to_async
def get_course_questions(course):
    return list(Question.objects.select_related('course').only(
        'id', 'course__id', 'marks', 'question', 'img_quiz',
        'option1', 'option2', 'option3', 'option4', 'answer'
    ).filter(course=course).order_by('id'))

@sync_to_async
def check_result_exists(profile, course):
    return Result.objects.select_related('student', 'exam').only(
        'student__id', 'student__username', 'exam_type__name',
        'exam__id', 'exam__course_name'
    ).filter(student=profile, exam=course).exists()

@sync_to_async
def get_or_create_shuffled_questions(student, course, all_questions):
    all_question_ids = [q.id for q in all_questions]

    session, created = StudentExamSession.objects.get_or_create(
        student=student,
        course=course,
        defaults={
            'question_order': random.sample(all_question_ids, len(all_question_ids))
        }
    )

    # Refresh the question order if mismatched (e.g. new questions added)
    if not created and set(session.question_order) != set(all_question_ids):
        session.question_order = random.sample(all_question_ids, len(all_question_ids))
        session.save()

    # Fetch the ordered questions
    ordered_questions = list(Question.objects.filter(id__in=session.question_order))
    ordered_questions.sort(key=lambda q: session.question_order.index(q.id))
    return ordered_questions

# Django sync views wrapped in async
async_render = sync_to_async(render, thread_sensitive=True)
async_redirect = sync_to_async(redirect, thread_sensitive=True)



from django.db.models import F
from django.db import transaction
from django.db import IntegrityError, transaction
from django.db import transaction

@csrf_exempt
def calculate_marks_view(request):
    if not request.user.is_authenticated:
        return redirect('account_login')   # Redirect to login if not authenticated
    return async_to_sync(_calculate_marks_async)(request)


async def _calculate_marks_async(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})

    course_id = request.COOKIES.get('course_id')
    if not course_id:
        return JsonResponse({'success': False, 'error': 'Course ID not found in cookies.'})

    try:
        answers_dict = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON format.'})

    try:
        course, student, result_exists, questions = await get_course_and_student_and_questions(course_id, request.user.id)
    except QMODEL.Course.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Course not found.'})
    except Profile.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student profile not found.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Unexpected error: {str(e)}'})

    # If result already exists, redirect immediately
    # if result_exists:
    #     return redirect('sms:certificates', pk=course.id)

    # Calculate marks
    total_marks = 0
    for question in questions:
        qid = str(question.id)
        selected = answers_dict.get(qid)
        if selected and selected == question.answer:
            total_marks += question.marks or 0

    try:
        await save_result(course, student, total_marks)
        # ✅ Redirect to certificate detail after saving result
        return redirect('certificates', pk=course.id)
    except IntegrityError:
        return redirect('certificates', pk=course.id)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Unexpected error: {str(e)}'})


@sync_to_async
def get_course_and_student_and_questions(course_id, user_id):
    course = QMODEL.Course.objects.select_related(
        'schools', 'session', 'term', 'exam_type'
    ).get(id=course_id)
    student = Profile.objects.select_related('user').get(user_id=user_id)

    result_exists = QMODEL.Result.objects.filter(
        student=student,
        exam=course,
        session=course.session,
        term=course.term,
        exam_type=course.exam_type,
    ).exists()

    questions = list(QMODEL.Question.objects.filter(course=course).order_by('id'))

    return course, student, result_exists, questions


@sync_to_async
def save_result(course, student, total_marks):
    """
    Create a new Result if it doesn't exist, or update the marks if it does.
    """
    with transaction.atomic():
        result, created = QMODEL.Result.objects.get_or_create(
            student=student,
            exam=course,
            session=course.session,
            term=course.term,
            exam_type=course.exam_type,
            defaults={'schools': course.schools, 'marks': total_marks}
        )
        if not created:
            # Update the existing result with the new marks
            result.marks = total_marks
            result.save()

# @sync_to_async
# def save_result(course, student, total_marks):
#     with transaction.atomic():
#         QMODEL.Result.objects.create(
#             schools=course.schools,
#             marks=total_marks,
#             exam=course,
#             session=course.session,
#             term=course.term,
#             exam_type=course.exam_type,
#             student=student,
#         )


#working with async views
# @csrf_exempt
# def calculate_marks_view(request):
#     if not request.user.is_authenticated:
#         return JsonResponse({'success': False, 'error': 'Authentication required.'}, status=401)
#     return async_to_sync(_calculate_marks_async)(request)


# async def _calculate_marks_async(request):
#     if request.method != 'POST':
#         return JsonResponse({'success': False, 'error': 'Invalid request method.'})

#     course_id = request.COOKIES.get('course_id')
#     if not course_id:
#         return JsonResponse({'success': False, 'error': 'Course ID not found in cookies.'})

#     try:
#         answers_dict = json.loads(request.body)
#     except json.JSONDecodeError:
#         return JsonResponse({'success': False, 'error': 'Invalid JSON format.'})

#     try:
#         course, student, result_exists, questions = await get_course_and_student_and_questions(course_id, request.user.id)
#     except QMODEL.Course.DoesNotExist:
#         return JsonResponse({'success': False, 'error': 'Course not found.'})
#     except Profile.DoesNotExist:
#         return JsonResponse({'success': False, 'error': 'Student profile not found.'})
#     except Exception as e:
#         return JsonResponse({'success': False, 'error': f'Unexpected error: {str(e)}'})

#     if result_exists:
#         return JsonResponse({'success': False, 'error': 'Result already exists.'})

#     total_marks = 0

#     for question in questions:
#         qid = str(question.id)
#         selected = answers_dict.get(qid)

#         if selected and selected == question.answer:
#             total_marks += question.marks or 0

#     try:
#         await save_result(course, student, total_marks)
#         return JsonResponse({'success': True, 'message': 'Quiz graded and saved ✅'})
#     except IntegrityError:
#         return JsonResponse({'success': False, 'error': 'Result already exists.'})
#     except Exception as e:
#         return JsonResponse({'success': False, 'error': f'Unexpected error: {str(e)}'})


# @sync_to_async
# def get_course_and_student_and_questions(course_id, user_id):
#     course = QMODEL.Course.objects.select_related('schools', 'session', 'term', 'exam_type').get(id=course_id)
#     student = Profile.objects.select_related('user').get(user_id=user_id)

#     result_exists = QMODEL.Result.objects.filter(
#         student=student,
#         exam=course,
#         session=course.session,
#         term=course.term,
#         exam_type=course.exam_type,
        
#     ).exists()

#     questions = list(QMODEL.Question.objects.filter(course=course).order_by('id'))

#     return course, student, result_exists, questions


# @sync_to_async
# def save_result(course, student, total_marks):
#     with transaction.atomic():
#         QMODEL.Result.objects.create(
#             schools=course.schools,
#             marks=total_marks,
#             exam=course,
#             session=course.session,
#             term=course.term,
#             exam_type=course.exam_type,
#             student=student,
            
#         )


# @login_required
# def start_exams_view(request, pk):
#     course = QMODEL.Course.objects.get(id=pk)
#     questions = QMODEL.Question.objects.filter(course=course).order_by('id')
#     q_count = questions.count()
#     paginator = Paginator(questions, 200)  # Show 100 questions per page.
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
    
#     # Calculate quiz end time
#     quiz_duration = course.duration_minutes
#     quiz_start_time = timezone.now()
#     quiz_end_time = quiz_start_time + timedelta(minutes=quiz_duration)
    
#     # Store the quiz end time in cache
#     cache.set(f'quiz_end_time_{course.id}', quiz_end_time, timeout=None)

#     # Calculate remaining time until the end of the quiz
#     remaining_time = quiz_end_time - timezone.now()
#     remaining_seconds = max(int(remaining_time.total_seconds()), 0)

#     context = {
#         'course': course,
#         'questions': questions,
#         'q_count': q_count,
#         'page_obj': page_obj,
#         'remaining_seconds': remaining_seconds,  # Pass remaining time to template
#     }

#     if request.method == 'POST':
#         # Handle form submission
#         pass

#     response = render(request, 'student/dashboard/start_exams.html', context=context)
#     response.set_cookie('course_id', course.id)
#     return response


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

from django.db.models import F
from django.db import transaction
from django.db import IntegrityError, transaction
from django.db import transaction



# @login_required
# def calculate_marks_view(request):
#     if request.COOKIES.get('course_id') is not None:
#         course_id = request.COOKIES.get('course_id')
#         course = QMODEL.Course.objects.get(id=course_id)
        
#         total_marks = 0
#         questions = QMODEL.Question.objects.filter(course=course).order_by('id')
        
#         if request.body:
#             json_data = json.loads(request.body)
#             for i, question in enumerate(questions, start=1):
#                 selected_ans = json_data.get(str(i))
#                 print("answers" + str(i), selected_ans)
#                 actual_answer = question.answer
#                 if selected_ans == actual_answer:
#                     total_marks += question.marks
        
#         student = Profile.objects.get(user_id=request.user.id)
#         result = QMODEL.Result.objects.create(marks=total_marks, exam=course, student=student)
        
#         # Redirect to the view_result URL
#         return JsonResponse({'success': True, 'message': 'Marks calculated successfully.'})
    
#     else:
#         return JsonResponse({'success': False, 'error': 'Course ID not found.'})



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
    qcourses = Course.objects.only('id').order_by('id')
    context = {
        'courses': qcourses
    }
    return render(request, 'student/dashboard/view_result.html', context)



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






   
   
#     return response
from django.urls import reverse
import uuid
from django.views.generic import TemplateView


import logging
logger = logging.getLogger(__name__)


def verify_certificate(request, code):
    # Retrieve the certificate using the code
    certificate = get_object_or_404(Certificate, code=code)

     # Generate the verification link for the certificate
    verification_link = request.build_absolute_uri(
        reverse('student:verify_certificate', args=[certificate.code])
    )
    

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
from certificate_stats.models import CertificateDownload, CourseCertificateCount  # make sure this imports your tracking model



  

# class BorderFlowable(Flowable):
#     def __init__(self, width, height):
#         Flowable.__init__(self)
#         self.width = width
#         self.height = height

#     def draw(self):
#         c = self.canv
#         c.setStrokeColor(colors.HexColor("#4C6DC9"))
#         c.setLineWidth(4)
#         c.rect(10, 10, self.width - 20, self.height - 20)
#         c.setLineWidth(1.5)
#         c.rect(16, 16, self.width - 32, self.height - 32)


def _get_or_create_certificate(user_newuser, course):
    try:
        cert, _ = Certificate.objects.get_or_create(
            user=user_newuser,
            course=course,
            defaults={
                'verification_code': uuid.uuid4(),
                'code': uuid.uuid4().hex[:8],
            }
        )
    except MultipleObjectsReturned:
        cert = Certificate.objects.filter(user=user_newuser, course=course).first()
    return cert


def pdf_id_view(request, pk):
    # ✅ Fixed: Courses not Course
    course = get_object_or_404(Course, pk=pk)

    # ✅ Fixed: course.title not course.course_name.title
    course_cert_count, _ = CourseCertificateCount.objects.get_or_create(
        title=str(course.course_name.title)

    )

    if request.user.is_authenticated:
        user_newuser, _ = NewUser.objects.get_or_create(email=request.user.email)
        certificate = _get_or_create_certificate(user_newuser, course)
    else:
        try:
            certificate, _ = Certificate.objects.get_or_create(
                course=course,
                defaults={
                    'verification_code': uuid.uuid4(),
                    'code': uuid.uuid4().hex[:8],
                }
            )
        except MultipleObjectsReturned:
            certificate = Certificate.objects.filter(course=course).first()

    CertificateDownload.objects.create(
        certificate=course_cert_count,
        user=request.user if request.user.is_authenticated else None
    )

    user = certificate.user
    school = user.school if user and hasattr(user, 'school') else None

    verification_url = request.build_absolute_uri(
        reverse('student:verify_certificate', args=[certificate.code])
    )

    logo_obj = Logo.objects.first()
    sign_obj = Signature.objects.first()

    # ✅ Raw Cloudinary URLs — NO build_absolute_uri wrapping
    logo_url = logo_obj.logo.url if logo_obj and logo_obj.logo else None
    sign_url = sign_obj.sign.url if sign_obj and sign_obj.sign else None

    print(f"[DEBUG] logo_url: {logo_url}")
    print(f"[DEBUG] sign_url: {sign_url}")

    context = {
        'first_name':        str(user.first_name) if user else 'Anonymous',
        'last_name':         str(user.last_name)  if user else '',
        # ✅ Fixed: course.title not course.course_name.title
        'course_name':       str(course.course_name.title) if course and course.course_name else 'Unknown Course',
        'date':              timezone.now(),
        'school_name':       str(school.school_name) if school else '',
        'principal_name':    str(school.name)        if school else '',
        'verification_url':  str(verification_url),
        'verification_code': str(certificate.code),
        # ✅ Fixed: raw Cloudinary URL, no build_absolute_uri
        'logo_url':          logo_url,
        'sign_url':          sign_url,
        'school_logo_url': school.logo.url if school and school.logo else None,
        'school_sign_url': school.principal_signature.url if school and school.principal_signature else None,
    }

    pdf_buffer = generate_certificate_pdf(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="certificate.pdf"'
    response.write(pdf_buffer.getvalue())
    return response

# def _fetch_image_from_url(url: str, width, height):
#     try:
#         print(f"[DEBUG] Fetching image from: {url}")
#         resp = requests.get(url, timeout=10)
#         resp.raise_for_status()
#         print(f"[DEBUG] Status: {resp.status_code}, Size: {len(resp.content)} bytes")
#         img = Image(BytesIO(resp.content), width=width, height=height)
#         img.hAlign = 'CENTER'
#         return img
#     except Exception as e:
#         print(f"[DEBUG] Image fetch failed: {e}")
#         return None


# from reportlab.lib.utils import ImageReader
# import math
# from io import BytesIO
# from datetime import date
# import requests

# from reportlab.lib import colors
# from reportlab.lib.pagesizes import A4, landscape
# from reportlab.lib.units import mm
# from reportlab.pdfgen import canvas as rl_canvas
# from reportlab.lib.utils import ImageReader

# import math
# from io import BytesIO
# from datetime import date
# import requests

# from reportlab.lib import colors
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.units import mm
# from reportlab.pdfgen import canvas as rl_canvas
# from reportlab.lib.utils import ImageReader
# #portrait orientation
# # ── Palette ───────────────────────────────────────────────────────────────────
# BLUE_DARK  = colors.HexColor('#1E3A8A')
# BLUE_MID   = colors.HexColor('#2563EB')
# BLUE_LIGHT = colors.HexColor('#DBEAFE')
# TEAL       = colors.HexColor('#0EA5E9')
# WHITE      = colors.HexColor('#FFFFFF')
# OFF_WHITE  = colors.HexColor('#F8FAFC')
# DARK_TEXT  = colors.HexColor('#0F172A')
# BODY_TEXT  = colors.HexColor('#334155')
# MUTED      = colors.HexColor('#94A3B8')
# LINE_LIGHT = colors.HexColor('#E2E8F0')
# GOLD       = colors.HexColor('#F59E0B')
# GOLD_LIGHT = colors.HexColor('#FCD34D')


def _r(col):
    return col.red, col.green, col.blue


# def draw_background(c, pw, ph):
#     # White base
#     c.setFillColor(WHITE)
#     c.rect(0, 0, pw, ph, fill=1, stroke=0)

#     # Off-white inner panel
#     c.setFillColor(OFF_WHITE)
#     c.rect(32, 32, pw - 64, ph - 64, fill=1, stroke=0)

#     # Subtle dot-grid watermark
#     c.setFillColor(colors.Color(*_r(BLUE_MID), alpha=0.04))
#     for x in range(48, int(pw - 36), 13):
#         for y in range(48, int(ph - 36), 13):
#             c.circle(x, y, 0.75, fill=1, stroke=0)

#     # Faint concentric circles at vertical center
#     c.setFillColor(colors.Color(1, 1, 1, alpha=0))
#     for r in [55, 78, 101]:
#         c.setStrokeColor(colors.Color(*_r(BLUE_MID), alpha=0.05))
#         c.setLineWidth(0.7)
#         c.circle(pw / 2, ph / 2, r, fill=0, stroke=1)

#     # Faint "CT" watermark
#     c.saveState()
#     c.setFillColor(colors.Color(*_r(BLUE_DARK), alpha=0.025))
#     c.setFont('Helvetica-Bold', 110)
#     c.drawCentredString(pw / 2, ph / 2 - 38, "CT")
#     c.restoreState()

#     # Corner fan patterns
#     c.saveState()
#     c.setStrokeColor(colors.Color(*_r(BLUE_MID), alpha=0.05))
#     c.setLineWidth(0.4)
#     for (fx, fy), start in [
#         ((38, 38), 0), ((pw - 38, 38), 90),
#         ((38, ph - 38), 270), ((pw - 38, ph - 38), 180)
#     ]:
#         for off in range(0, 91, 10):
#             a = math.radians(start + off)
#             c.line(fx, fy, fx + 38 * math.cos(a), fy + 38 * math.sin(a))
#     c.restoreState()


# def draw_border(c, pw, ph):
#     # Outer navy line
#     c.setStrokeColor(BLUE_DARK)
#     c.setLineWidth(1.5)
#     c.rect(10, 10, pw - 20, ph - 20)

#     # Inner pale blue line
#     c.setStrokeColor(BLUE_LIGHT)
#     c.setLineWidth(0.6)
#     c.rect(14, 14, pw - 28, ph - 28)

#     # L-bracket corners
#     bl = 20
#     c.setStrokeColor(BLUE_MID)
#     c.setLineWidth(2)
#     for (bx, by, dx, dy) in [
#         (10, ph - 10,  1, -1),
#         (pw - 10, ph - 10, -1, -1),
#         (10, 10,  1,  1),
#         (pw - 10, 10, -1,  1),
#     ]:
#         c.line(bx, by, bx + dx * bl, by)
#         c.line(bx, by, bx, by + dy * bl)

#     # Filled corner squares
#     sq = 4
#     c.setFillColor(BLUE_DARK)
#     for sx, sy in [(10, 10), (pw - 10 - sq, 10),
#                    (10, ph - 10 - sq), (pw - 10 - sq, ph - 10 - sq)]:
#         c.rect(sx, sy, sq, sq, fill=1, stroke=0)


# def draw_header_band(c, pw, ph, band_h, logo_img=None, logo_aspect=3.0):
#     band_y = ph - 18 - band_h
#     # Navy fill
#     c.setFillColor(BLUE_DARK)
#     c.rect(18, band_y, pw - 36, band_h, fill=1, stroke=0)
#     # Teal bottom strip
#     c.setFillColor(TEAL)
#     c.rect(18, band_y, pw - 36, 3, fill=1, stroke=0)
#     # Gold line below teal
#     c.setFillColor(GOLD)
#     c.rect(18, band_y - 2, pw - 36, 1.5, fill=1, stroke=0)

#     # Decorative left circles
#     mid_y = band_y + band_h / 2
#     c.setFillColor(TEAL)
#     c.circle(30, mid_y, 5, fill=1, stroke=0)
#     c.setFillColor(GOLD)
#     c.circle(40, mid_y, 3, fill=1, stroke=0)

#     if logo_img:
#         # Logo left-aligned inside band
#         logo_h = band_h - 4
#         logo_w = logo_h * logo_aspect
#         c.drawImage(logo_img, 50, band_y + 2,
#                     width=logo_w, height=logo_h,
#                     mask='auto', preserveAspectRatio=True)
#         # Academy name centered
#         c.setFillColor(WHITE)
#         c.setFont('Helvetica-Bold', 10)
#         c.drawCentredString(pw / 2, band_y + band_h / 2 - 4, "CODETHINKERS ACADEMY")
#     else:
#         # Academy name centered
#         c.setFillColor(WHITE)
#         c.setFont('Helvetica-Bold', 11)
#         c.drawCentredString(pw / 2, band_y + band_h / 2 - 4, "CODETHINKERS ACADEMY")

#     # Tagline right-aligned
#     c.setFillColor(colors.Color(*_r(BLUE_LIGHT), alpha=0.7))
#     c.setFont('Helvetica', 6.5)
#     c.drawRightString(pw - 24, band_y + band_h / 2 - 4,
#                       "Excellence in Technology Education  ·")


# def draw_footer_band(c, pw, ph):
#     c.setFillColor(BLUE_DARK)
#     c.rect(18, 18, pw - 36, 10, fill=1, stroke=0)
#     c.setFillColor(TEAL)
#     c.rect(18, 28, pw - 36, 2.5, fill=1, stroke=0)


# def draw_side_bars(c, pw, ph, band_h):
#     """Thin vertical navy bars on left and right."""
#     bar_w = 6
#     top = ph - 18 - band_h
#     bot = 32
#     height = top - bot

#     for bx in [18, pw - 18 - bar_w]:
#         c.setFillColor(BLUE_DARK)
#         c.rect(bx, bot, bar_w, height, fill=1, stroke=0)
#         # Teal accent segments at 25%, 50%, 75%
#         for t in [0.25, 0.5, 0.75]:
#             sy = bot + height * t - 7
#             c.setFillColor(TEAL)
#             c.rect(bx, sy, bar_w, 14, fill=1, stroke=0)
#             c.setFillColor(GOLD)
#             c.circle(bx + bar_w / 2, bot + height * t, 2.2, fill=1, stroke=0)


# def draw_badge(c, cx, cy, r=22):
#     """Circular CT badge."""
#     c.setStrokeColor(BLUE_MID)
#     c.setFillColor(colors.Color(1, 1, 1, alpha=0))
#     c.setLineWidth(2)
#     c.circle(cx, cy, r, fill=0, stroke=1)
#     c.setStrokeColor(GOLD)
#     c.setLineWidth(0.8)
#     c.circle(cx, cy, r - 3, fill=0, stroke=1)
#     c.setFillColor(BLUE_DARK)
#     c.circle(cx, cy, r - 4.5, fill=1, stroke=0)
#     c.setFillColor(WHITE)
#     c.setFont('Helvetica-Bold', 11)
#     c.drawCentredString(cx, cy - 4, "CT")
#     # Tick marks
#     c.setStrokeColor(GOLD_LIGHT)
#     c.setLineWidth(0.5)
#     for i in range(24):
#         a = math.radians(i * 15)
#         c.line(cx + (r - 0.5) * math.cos(a), cy + (r - 0.5) * math.sin(a),
#                cx + (r - 2.5) * math.cos(a), cy + (r - 2.5) * math.sin(a))


# def draw_divider(c, cx, cy, w, color=BLUE_MID):
#     half = w / 2
#     c.setStrokeColor(color)
#     c.setLineWidth(0.7)
#     c.line(cx - half, cy, cx - 6, cy)
#     c.line(cx + 6, cy, cx + half, cy)
#     c.setFillColor(color)
#     c.circle(cx, cy, 2.5, fill=1, stroke=0)
#     c.setFillColor(WHITE)
#     c.circle(cx, cy, 1.2, fill=1, stroke=0)


# def generate_certificate_pdf(ctx: dict) -> BytesIO:
#     buffer = BytesIO()
#     # ── Portrait A4 ──────────────────────────────────────────────────────────
#     pw, ph = A4   # 595 x 842 pts  (210mm x 297mm)
#     c = rl_canvas.Canvas(buffer, pagesize=A4)

#     band_h = 11 * mm

#     # Load logo once if provided
#     logo_img = None
#     logo_aspect = 3.0
#     if ctx.get('logo_url'):
#         try:
#             url = ctx['logo_url']
#             if url.startswith('file://'):
#                 logo_img = ImageReader(url.replace('file://', ''))
#             else:
#                 resp = requests.get(url, timeout=10)
#                 resp.raise_for_status()
#                 logo_img = ImageReader(BytesIO(resp.content))
#         except Exception as e:
#             print(f"[DEBUG] Logo: {e}")

#     draw_background(c, pw, ph)
#     draw_border(c, pw, ph)
#     draw_header_band(c, pw, ph, band_h, logo_img, logo_aspect)
#     draw_footer_band(c, pw, ph)
#     draw_side_bars(c, pw, ph, band_h)

#     # Badges — left and right of centre, just below header
#     badge_y = ph - 18 - band_h - 28
#     draw_badge(c, 42, badge_y, r=18)
#     draw_badge(c, pw - 42, badge_y, r=18)

#     cx = pw / 2

#     # ── Calculate total content height to center everything vertically ─────────
#     # Content area: from just below header to just above footer
#     content_top = ph - 18 - band_h - 10
#     content_bot = 52   # above footer pill
#     content_h   = content_top - content_bot

#     # Fixed block heights (pts)
#     EYEBROW_H  = 10
#     DIV_H      = 8
#     TITLE_H    = 40   # 34pt font + descender
#     UNDERLINE_H= 8
#     CERTIFY_H  = 14
#     NAME_H     = 42   # 34pt font
#     NAME_UL_H  = 8
#     BODY_H     = 14
#     COURSE_H   = 22   # 15pt bold
#     COURSE_UL_H= 8
#     DATE_H     = 14
#     DIV2_H     = 8
#     SIG_IMG_H  = 10 * mm if ctx.get('sign_url') else 0
#     SIG_LINE_H = 6
#     SIG_NAME_H = 13
#     SIG_TITLE_H= 12

#     total_block = (EYEBROW_H + DIV_H + TITLE_H + UNDERLINE_H +
#                    CERTIFY_H + NAME_H + NAME_UL_H + BODY_H +
#                    COURSE_H + COURSE_UL_H + DATE_H + DIV2_H +
#                    SIG_IMG_H + SIG_LINE_H + SIG_NAME_H + SIG_TITLE_H)

#     # Distribute remaining space evenly as padding between 10 gaps
#     n_gaps  = 10
#     gap     = max((content_h - total_block) / n_gaps, 8)

#     y = content_top

#     # ── Eyebrow ───────────────────────────────────────────────────────────────
#     c.setFillColor(TEAL)
#     c.setFont('Helvetica-Bold', 7.5)
#     c.drawCentredString(cx, y, "· CERTIFICATE OF COMPLETION ·")
#     y -= EYEBROW_H + gap * 0.6

#     draw_divider(c, cx, y, 220, BLUE_LIGHT)
#     y -= DIV_H + gap * 0.6

#     # ── Main title ────────────────────────────────────────────────────────────
#     c.setFillColor(DARK_TEXT)
#     c.setFont('Times-BoldItalic', 34)
#     c.drawCentredString(cx, y, "Certificate of Completion")
#     y -= TITLE_H

#     # Double underline
#     c.setStrokeColor(BLUE_MID)
#     c.setLineWidth(1.5)
#     c.line(cx - 120, y, cx + 120, y)
#     c.setStrokeColor(GOLD)
#     c.setLineWidth(0.6)
#     c.line(cx - 80, y - 3, cx + 80, y - 3)
#     y -= UNDERLINE_H + gap

#     # ── Certify ───────────────────────────────────────────────────────────────
#     c.setFillColor(MUTED)
#     c.setFont('Helvetica', 10)
#     c.drawCentredString(cx, y, "This is to proudly certify that")
#     y -= CERTIFY_H + gap

#     # ── Student name ──────────────────────────────────────────────────────────
#     full_name = f"{ctx['first_name']} {ctx['last_name']}".strip()
#     c.setFillColor(BLUE_DARK)
#     c.setFont('Times-BoldItalic', 34)
#     c.drawCentredString(cx, y, full_name)
#     y -= NAME_H

#     # Gold underline for name
#     nw = min(len(full_name) * 9.8, 260)
#     c.setStrokeColor(GOLD)
#     c.setLineWidth(2)
#     c.line(cx - nw / 2, y, cx + nw / 2, y)
#     c.setStrokeColor(GOLD_LIGHT)
#     c.setLineWidth(0.5)
#     c.line(cx - nw / 2 + 10, y - 3, cx + nw / 2 - 10, y - 3)
#     y -= NAME_UL_H + gap

#     # ── Body ──────────────────────────────────────────────────────────────────
#     c.setFillColor(BODY_TEXT)
#     c.setFont('Helvetica', 10)
#     c.drawCentredString(cx, y, "has successfully completed the course")
#     y -= BODY_H + gap

#     # ── Course name ───────────────────────────────────────────────────────────
#     c.setFillColor(BLUE_MID)
#     c.setFont('Helvetica-Bold', 15)
#     c.drawCentredString(cx, y, ctx['course_name'])
#     y -= COURSE_H

#     cw = min(len(ctx['course_name']) * 7.8, 280)
#     c.setStrokeColor(TEAL)
#     c.setLineWidth(1.2)
#     c.line(cx - cw / 2, y, cx + cw / 2, y)
#     y -= COURSE_UL_H + gap

#     # ── Date ─────────────────────────────────────────────────────────────────
#     date_str = ctx['date'].strftime('%B %d, %Y')
#     c.setFillColor(MUTED)
#     c.setFont('Helvetica', 9.5)
#     c.drawCentredString(cx, y, f"Awarded on  {date_str}")
#     y -= DATE_H + gap

#     draw_divider(c, cx, y, 240, LINE_LIGHT)
#     y -= DIV2_H + gap

#     # ── Signature block ───────────────────────────────────────────────────────
#     if ctx.get('sign_url'):
#         try:
#             resp = requests.get(ctx['sign_url'], timeout=10)
#             resp.raise_for_status()
#             img = ImageReader(BytesIO(resp.content))
#             c.drawImage(img, cx - 15 * mm, y - 10 * mm,
#                         width=30 * mm, height=10 * mm,
#                         mask='auto', preserveAspectRatio=True)
#             y -= 10 * mm + 6
#         except Exception as e:
#             print(f"[DEBUG] Sig: {e}")

#     c.setStrokeColor(BLUE_DARK)
#     c.setLineWidth(1)
#     c.line(cx - 50, y, cx + 50, y)
#     y -= SIG_LINE_H + 6

#     c.setFillColor(DARK_TEXT)
#     c.setFont('Helvetica-Bold', 9)
#     c.drawCentredString(cx, y, ctx.get('principal_name', 'Director of Education'))
#     y -= SIG_NAME_H

#     c.setFillColor(MUTED)
#     c.setFont('Helvetica', 7.5)
#     c.drawCentredString(cx, y, "Authorized Signatory")

#     # ── Verification footer ───────────────────────────────────────────────────
#     verify_text = f"Verify at: {ctx['verification_url']}   |   Certificate ID: {ctx['verification_code']}"
#     pill_w = 300
#     pill_h = 14
#     pill_x = cx - pill_w / 2
#     pill_y = 34

#     c.setFillColor(WHITE)
#     c.roundRect(pill_x, pill_y, pill_w, pill_h, 5, fill=1, stroke=0)
#     c.setStrokeColor(BLUE_LIGHT)
#     c.setLineWidth(0.6)
#     c.roundRect(pill_x, pill_y, pill_w, pill_h, 5, fill=0, stroke=1)
#     c.setFillColor(TEAL)
#     c.circle(cx, pill_y + pill_h / 2, 2, fill=1, stroke=0)
#     c.setFillColor(WHITE)
#     c.circle(cx, pill_y + pill_h / 2, 1, fill=1, stroke=0)
#     c.setFillColor(BODY_TEXT)
#     c.setFont('Helvetica', 6.5)
#     c.drawCentredString(cx, pill_y + 4, verify_text)

#     c.save()
#     buffer.seek(0)
#     return buffer


# # ── Demo ──────────────────────────────────────────────────────────────────────
# if __name__ == '__main__':
#     ctx = {
#         'first_name': 'Alexandra',
#         'last_name': 'Johnson',
#         'course_name': 'Full-Stack Web Development with Python & React',
#         'date': date(2025, 6, 15),
#         'school_name': 'CodeThinkers Academy',
#         'principal_name': 'Dr. Samuel Okonkwo',
#         'verification_url': 'https://verify.codethinkers.academy',
#         'verification_code': 'CTA-2025-78F3A9',
#         'logo_url': None,
#         'sign_url': None,
#     }

#     pdf_buf = generate_certificate_pdf(ctx)
#     with open('/mnt/user-data/outputs/certificate_portrait.pdf', 'wb') as f:
#         f.write(pdf_buf.read())
#     print("Done → certificate_portrait.pdf")

#landscape(A4) => (842.0, 595.0)
# ── Palette: Modern Minimalist ───────────────────────────────────────────────

import os
import math
import requests
from io import BytesIO
from datetime import date

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.utils import ImageReader


# ── Palette ───────────────────────────────────────────────────────────────────
BLUE_DARK  = colors.HexColor('#1E3A8A')
BLUE_MID   = colors.HexColor('#2563EB')
BLUE_LIGHT = colors.HexColor('#DBEAFE')
TEAL       = colors.HexColor('#0EA5E9')
WHITE      = colors.HexColor('#FFFFFF')
OFF_WHITE  = colors.HexColor('#F8FAFC')
DARK_TEXT  = colors.HexColor('#0F172A')
BODY_TEXT  = colors.HexColor('#334155')
MUTED      = colors.HexColor('#94A3B8')
LINE_LIGHT = colors.HexColor('#E2E8F0')
GOLD       = colors.HexColor('#C9960C')
GOLD_MID   = colors.HexColor('#E8B020')
GOLD_LIGHT = colors.HexColor('#F5D060')
GOLD_PALE  = colors.HexColor('#FDE68A')


# ── Robust Logo Loader1 ───────────────────────────────────────────────────────
def load_image(image_url):
    """Load image from local path or URL"""
    if not image_url:
        return None

    try:
        # Absolute local path
        if os.path.exists(image_url):
            return ImageReader(image_url)

        # HTTP/HTTPS URL
        if image_url.startswith('http'):
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            print(f"[DEBUG] Loaded image: {image_url}")
            return ImageReader(BytesIO(response.content))

        # file:// format
        if image_url.startswith('file://'):
            return ImageReader(image_url.replace('file://', ''))

    except Exception as e:
        print(f"[DEBUG] Image load error: {e}")

    return None

def _r(col):
    return col.red, col.green, col.blue

# ── Graduation Celebration Badge ─────────────────────────────────────────────
def draw_award_badge(c, cx, cy, r=28):
    """
    Graduation-themed celebration seal:
    - Starburst spikes radiating outward (celebration burst)
    - Gold medal disc with laurel leaves
    - Mortarboard cap on top
    - Navy ribbon tails below
    """

    # ── Navy ribbon tails (behind everything) ────────────────────────────────
    c.setFillColor(BLUE_DARK)
    for dx in [-1, 1]:
        p = c.beginPath()
        p.moveTo(cx + dx * r * 0.15, cy - r * 0.75)
        p.lineTo(cx + dx * r * 0.55, cy - r * 0.45)
        p.lineTo(cx + dx * r * 0.65, cy + r * 0.55)   # pointed tip
        p.lineTo(cx + dx * r * 0.05, cy + r * 0.15)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
    # Gold edge highlights on ribbons
    c.setStrokeColor(GOLD_MID)
    c.setLineWidth(0.7)
    for dx in [-1, 1]:
        c.line(cx + dx*r*0.15, cy - r*0.75, cx + dx*r*0.65, cy + r*0.55)

    # ── Starburst spikes (celebration burst) ─────────────────────────────────
    spike_count = 20
    r_out = r * 1.18
    r_in  = r * 0.92
    c.setFillColor(GOLD_LIGHT)
    burst = c.beginPath()
    for i in range(spike_count * 2):
        angle = math.radians(i * 180 / spike_count - 90)
        sr    = r_out if i % 2 == 0 else r_in
        sx, sy = cx + sr * math.cos(angle), cy + sr * math.sin(angle)
        if i == 0: burst.moveTo(sx, sy)
        else:      burst.lineTo(sx, sy)
    burst.close()
    c.drawPath(burst, fill=1, stroke=0)

    # ── Outer gold ring ───────────────────────────────────────────────────────
    c.setFillColor(GOLD)
    c.circle(cx, cy, r * 0.90, fill=1, stroke=0)

    # ── Laurel wreath ring ────────────────────────────────────────────────────
    leaf_ring_r = r * 0.76
    leaf_count  = 24
    leaf_w, leaf_h = r * 0.12, r * 0.20
    c.setFillColor(GOLD_MID)
    for i in range(leaf_count):
        angle = math.radians(i * 360 / leaf_count)
        lx = cx + leaf_ring_r * math.cos(angle)
        ly = cy + leaf_ring_r * math.sin(angle)
        c.saveState()
        c.translate(lx, ly)
        c.rotate(math.degrees(angle) + 90)
        c.ellipse(-leaf_w/2, -leaf_h/2, leaf_w/2, leaf_h/2, fill=1, stroke=0)
        c.restoreState()

    # Inner navy disc
    c.setFillColor(BLUE_DARK)
    c.circle(cx, cy, r * 0.58, fill=1, stroke=0)

    # Inner gold ring accent
    c.setStrokeColor(GOLD_MID)
    c.setFillColor(colors.Color(1,1,1,alpha=0))
    c.setLineWidth(1)
    c.circle(cx, cy, r * 0.58, fill=0, stroke=1)

    # ── Mortarboard cap (graduation hat) ─────────────────────────────────────
    hat_w  = r * 0.52
    hat_h  = r * 0.18
    brim_h = r * 0.08
    hat_y  = cy + r * 0.12   # sit in upper part of disc

    # Board (flat top square — drawn as diamond rotated 0)
    c.setFillColor(GOLD)
    board_pts = [
        (cx,           hat_y + hat_h + brim_h * 0.6),   # top
        (cx + hat_w/2, hat_y + hat_h),                   # right
        (cx,           hat_y + hat_h - brim_h * 0.6),   # bottom
        (cx - hat_w/2, hat_y + hat_h),                   # left
    ]
    bp = c.beginPath()
    bp.moveTo(*board_pts[0])
    for pt in board_pts[1:]:
        bp.lineTo(*pt)
    bp.close()
    c.drawPath(bp, fill=1, stroke=0)

    # Cap body (trapezoid)
    c.setFillColor(GOLD_MID)
    cap_w_bot = hat_w * 0.55
    cap_w_top = hat_w * 0.30
    cp = c.beginPath()
    cp.moveTo(cx - cap_w_bot/2, hat_y)
    cp.lineTo(cx + cap_w_bot/2, hat_y)
    cp.lineTo(cx + cap_w_top/2, hat_y + hat_h)
    cp.lineTo(cx - cap_w_top/2, hat_y + hat_h)
    cp.close()
    c.drawPath(cp, fill=1, stroke=0)

    # Tassel string
    c.setStrokeColor(GOLD_LIGHT)
    c.setLineWidth(0.8)
    c.line(cx + hat_w * 0.18, hat_y + hat_h, cx + hat_w * 0.35, hat_y + hat_h * 0.3)
    # Tassel ball
    c.setFillColor(GOLD_LIGHT)
    c.circle(cx + hat_w * 0.35, hat_y + hat_h * 0.22, r * 0.05, fill=1, stroke=0)

    # ── "CT" monogram below cap ───────────────────────────────────────────────
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', r * 0.28)
    c.drawCentredString(cx, cy - r * 0.22, "CT")

    # ── Outer glow ring ───────────────────────────────────────────────────────
    c.setStrokeColor(GOLD_LIGHT)
    c.setFillColor(colors.Color(1,1,1,alpha=0))
    c.setLineWidth(1)
    c.circle(cx, cy, r * 0.91, fill=0, stroke=1)


def draw_background(c, pw, ph):
    c.setFillColor(WHITE)
    c.rect(0, 0, pw, ph, fill=1, stroke=0)
    c.setFillColor(OFF_WHITE)
    c.rect(36, 36, pw - 72, ph - 72, fill=1, stroke=0)

    # Dot grid
    c.setFillColor(colors.Color(*_r(BLUE_MID), alpha=0.04))
    for x in range(50, int(pw - 40), 14):
        for y in range(50, int(ph - 40), 14):
            c.circle(x, y, 0.8, fill=1, stroke=0)

    # Faint concentric circles
    c.setFillColor(colors.Color(1,1,1,alpha=0))
    for r in [55, 80, 105]:
        c.setStrokeColor(colors.Color(*_r(BLUE_MID), alpha=0.05))
        c.setLineWidth(0.7)
        c.circle(pw/2, ph/2, r, fill=0, stroke=1)

    # CT watermark
    c.saveState()
    c.setFillColor(colors.Color(*_r(BLUE_DARK), alpha=0.03))
    c.setFont('Helvetica-Bold', 120)
    c.drawCentredString(pw/2, ph/2 - 42, "CT")
    c.restoreState()


def draw_border(c, pw, ph):
    c.setStrokeColor(BLUE_DARK)
    c.setLineWidth(1.5)
    c.rect(10, 10, pw-20, ph-20)
    c.setStrokeColor(BLUE_LIGHT)
    c.setLineWidth(0.6)
    c.rect(14, 14, pw-28, ph-28)

    bl = 18
    c.setStrokeColor(BLUE_MID)
    c.setLineWidth(1.8)
    for (bx, by, dx, dy) in [
        (10, ph-10,  1, -1),
        (pw-10, ph-10, -1, -1),
        (10, 10,  1,  1),
        (pw-10, 10, -1,  1),
    ]:
        c.line(bx, by, bx+dx*bl, by)
        c.line(bx, by, bx, by+dy*bl)

    sq = 4
    c.setFillColor(BLUE_DARK)
    for sx, sy in [(10,10),(pw-10-sq,10),(10,ph-10-sq),(pw-10-sq,ph-10-sq)]:
        c.rect(sx, sy, sq, sq, fill=1, stroke=0)


def draw_header_band(c, pw, ph, band_h):
    band_y = ph - 18 - band_h
    c.setFillColor(BLUE_DARK)
    c.rect(18, band_y, pw-36, band_h, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(18, band_y, pw-36, 3, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(18, band_y-2, pw-36, 1.5, fill=1, stroke=0)

    mid_y = band_y + band_h/2
    c.setFillColor(TEAL)
    c.circle(28, mid_y, 5, fill=1, stroke=0)
    c.setFillColor(GOLD_MID)
    c.circle(38, mid_y, 3, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 11)
    c.drawCentredString(pw/2, band_y + band_h/2 - 4, "CODETHINKERS ACADEMY")

    c.setFillColor(colors.Color(*_r(BLUE_LIGHT), alpha=0.7))
    c.setFont('Helvetica', 6.5)
    c.drawRightString(pw-24, band_y + band_h/2 - 4, "Excellence in Technology Education  ·")


def draw_footer_band(c, pw, ph):
    c.setFillColor(BLUE_DARK)
    c.rect(18, 18, pw-36, 10, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(18, 28, pw-36, 2.5, fill=1, stroke=0)


def draw_side_bars(c, pw, ph, band_h):
    bar_w = 6
    top = ph - 18 - band_h
    bot = 30
    h   = top - bot
    for bx in [18, pw-18-bar_w]:
        c.setFillColor(BLUE_DARK)
        c.rect(bx, bot, bar_w, h, fill=1, stroke=0)
        for t in [0.25, 0.5, 0.75]:
            sy = bot + h*t - 7
            c.setFillColor(TEAL)
            c.rect(bx, sy, bar_w, 14, fill=1, stroke=0)
            c.setFillColor(GOLD_MID)
            c.circle(bx + bar_w/2, bot + h*t, 2.2, fill=1, stroke=0)


def draw_thin_divider(c, cx, cy, w, color=BLUE_MID):
    half = w/2
    c.setStrokeColor(color)
    c.setLineWidth(0.7)
    c.line(cx-half, cy, cx-6, cy)
    c.line(cx+6, cy, cx+half, cy)
    c.setFillColor(color)
    c.circle(cx, cy, 2.5, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.circle(cx, cy, 1.2, fill=1, stroke=0)



def generate_certificate_pdf(ctx: dict) -> BytesIO:
    buffer = BytesIO()
    pw, ph = landscape(A4)
    c = rl_canvas.Canvas(buffer, pagesize=landscape(A4))

    band_h = 11 * mm

    # ── Load Images ─────────────────────────────────────────
    print("[DEBUG] logo_url:", ctx.get("logo_url"))
    print("[DEBUG] sign_url:", ctx.get("sign_url"))

    logo_img = load_image(ctx.get("logo_url"))
    sign_img = load_image(ctx.get("sign_url"))

    print(f"[DEBUG] Logo loaded: {bool(logo_img)}, Sign loaded: {bool(sign_img)}")

    # ── Background Elements ─────────────────────────────────
    draw_background(c, pw, ph)
    draw_border(c, pw, ph)
    draw_header_band(c, pw, ph, band_h)
    draw_footer_band(c, pw, ph)
    draw_side_bars(c, pw, ph, band_h)

    cx = pw / 2

    # ── Calculate Initial Title Y ───────────────────────────
    y = ph - 18 - band_h - 22 - 15

    # ── Draw Title FIRST ────────────────────────────────────
    c.setFillColor(DARK_TEXT)
    c.setFont("Times-BoldItalic", 38)
    c.drawCentredString(cx, y, "Certificate of Completion")

    title_y = y  # real baseline of title

    # ── Draw Badge (Right Side) ─────────────────────────────
    draw_award_badge(c, pw - 115, title_y - 10, r=32)

    # ── Draw Logo (Left Side) ───────────────────────────────
    if logo_img:
        logo_w = 55
        logo_h = 55
        logo_x = 115 - logo_w / 2
        logo_y = title_y - logo_h / 2 - 12  # baseline correction

        print(f"[DEBUG] Drawing logo at x={logo_x}, y={logo_y}")
        c.setFillColor(colors.white)
        c.rect(logo_x, logo_y, logo_w, logo_h, fill=1, stroke=0)

        c.drawImage(
            logo_img,
            logo_x,
            logo_y,
            width=logo_w,
            height=logo_h,
            mask="auto",
            preserveAspectRatio=True,
        )

    # ── Continue Layout ─────────────────────────────────────
    y -= 14

    c.setStrokeColor(BLUE_MID)
    c.setLineWidth(1.5)
    c.line(cx - 130, y, cx + 130, y)

    c.setStrokeColor(GOLD_MID)
    c.setLineWidth(0.6)
    c.line(cx - 90, y - 3, cx + 90, y - 3)

    y -= 28

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10)
    c.drawCentredString(cx, y, "This is to proudly certify that")

    y -= 32

    full_name = f"{ctx['first_name']} {ctx['last_name']}".strip()
    c.setFillColor(BLUE_DARK)
    c.setFont("Times-BoldItalic", 36)
    c.drawCentredString(cx, y, full_name)

    y -= 10

    nw = min(len(full_name) * 10.5, 290)
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(cx - nw / 2, y, cx + nw / 2, y)

    c.setStrokeColor(GOLD_LIGHT)
    c.setLineWidth(0.5)
    c.line(cx - nw / 2 + 10, y - 3, cx + nw / 2 - 10, y - 3)

    y -= 28

    c.setFillColor(BODY_TEXT)
    c.setFont("Helvetica", 10)
    c.drawCentredString(cx, y, "has successfully completed the course")

    y -= 30

    c.setFillColor(BLUE_MID)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(cx, y, ctx["course_name"])

    y -= 10

    cw = min(len(ctx["course_name"]) * 8.5, 320)
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.2)
    c.line(cx - cw / 2, y, cx + cw / 2, y)

    y -= 26

    date_str = ctx["date"].strftime("%B %d, %Y")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 9.5)
    c.drawCentredString(cx, y, f"Awarded on  {date_str}")

    y -= 28

    draw_thin_divider(c, cx, y, 280, LINE_LIGHT)

    y -= 30

    # ── Signature ───────────────────────────────────────────
    if sign_img:
        c.drawImage(
            sign_img,
            cx - 15 * mm,
            y - 10 * mm,
            width=30 * mm,
            height=10 * mm,
            mask="auto",
            preserveAspectRatio=True,
        )
        y -= 10 * mm + 4

    c.setStrokeColor(BLUE_DARK)
    c.setLineWidth(1)
    c.line(cx - 48, y, cx + 48, y)

    y -= 11

    c.setFillColor(DARK_TEXT)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(cx, y, ctx.get("principal_name", ""))

    y -= 11

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(cx, y, "Authorized Signatory")

    # ── Verification Pill ───────────────────────────────────
    verify_text = f"Verify at: {ctx['verification_url']}   |   ID: {ctx['verification_code']}"

    pill_w, pill_h = 400, 14
    pill_x = cx - pill_w / 2
    pill_y = 32

    c.setFillColor(colors.white)
    c.roundRect(pill_x, pill_y, pill_w, pill_h, 5, fill=1, stroke=0)

    c.setStrokeColor(BLUE_LIGHT)
    c.setLineWidth(0.6)
    c.roundRect(pill_x, pill_y, pill_w, pill_h, 5, fill=0, stroke=1)

    c.setFillColor(BODY_TEXT)
    c.setFont("Helvetica", 6.5)
    c.drawCentredString(cx, pill_y + 4, verify_text)

    c.save()
    buffer.seek(0)
    return buffer    

# working now
# def pdf_id_view(request, pk):
#     # Ensure the course exists
#     course = get_object_or_404(Course, pk=pk)
#     certificate = None

#     # Get or create the CourseCertificateCount record for tracking downloads
#     course_cert_count, _ = CourseCertificateCount.objects.get_or_create(
#         title=course.course_name
#     )

#     if request.user.is_authenticated:
#         user_newuser, created = NewUser.objects.get_or_create(email=request.user.email)

#         try:
#             certificate, created = Certificate.objects.get_or_create(
#                 user=user_newuser,
#                 course=course,
#                 defaults={
#                     'verification_code': uuid.uuid4(),
#                     'code': uuid.uuid4().hex[:8]
#                 }
#             )
#         except MultipleObjectsReturned:
#             certificate = Certificate.objects.filter(user=user_newuser, course=course).first()

#         # Log the download for authenticated users
#         CertificateDownload.objects.create(
#             certificate=course_cert_count,  # <-- now using CourseCertificateCount
#             user=request.user
#         )

#     else:
#         try:
#             certificate, created = Certificate.objects.get_or_create(
#                 course=course,
#                 defaults={
#                     'verification_code': uuid.uuid4(),
#                     'code': uuid.uuid4().hex[:8]
#                 }
#             )
#         except MultipleObjectsReturned:
#             certificate = Certificate.objects.filter(course=course).first()

#         # Optional: log anonymous download
#         CertificateDownload.objects.create(
#             certificate=course_cert_count,  # <-- now using CourseCertificateCount
#             user=None
#         )

#     # Extra data for PDF
#     student = Profile.objects.filter(user_id=request.user.id).first() if request.user.is_authenticated else None
#     date = timezone.now()
#     logo = Logo.objects.all()
#     sign = Signature.objects.all()
#     design = Designcert.objects.all()

#     context = {
#         'results': [course],
#         'first_name': certificate.user.first_name if certificate.user else 'Anonymous',
#         'last_name': certificate.user.last_name if certificate.user else '',
#         'date': date,
#         'course': [course],
#         'logo': logo,
#         'sign': sign,
#         'design': design,
#         'school_name': certificate.user.school.school_name if certificate.user and certificate.user.school else '',
#         'school_logo': certificate.user.school.logo if certificate.user and certificate.user.school else '',
#         'school_sign': certificate.user.school.principal_signature if certificate.user and certificate.user.school else '',
#         'principal_name': certificate.user.school.name if certificate.user and certificate.user.school else '',
#         'portfolio': certificate.user.school.portfolio if certificate.user and certificate.user.school else '',
#         'verification_url': request.build_absolute_uri(
#             reverse('student:verify_certificate', args=[certificate.code])
#         ),
#     }

#     # Render PDF
#     template_path = 'student/dashboard/certificatepdf_testing.html'
#     template = get_template(template_path)
#     html = template.render(context)
    
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'inline; filename="certificate.pdf"'
    
#     pisa_status = pisa.CreatePDF(html, dest=response)
    
#     if pisa_status.err:
#         return HttpResponse(f'We had some errors <pre>{html}</pre>', status=500)

#     return response


# # original pdf
# def pdf_id_view(request, pk):
#     # Ensure the course associated with the certificate exists
#     course = get_object_or_404(Course, pk=pk)
#     certificate = None

#     if request.user.is_authenticated:
#         user_newuser, created = NewUser.objects.get_or_create(email=request.user.email)

#         try:
#             # Ensure a certificate for the user and course exists or create it if not
#             certificate, created = Certificate.objects.get_or_create(
#                 user=user_newuser,
#                 course=course,
#                 defaults={
#                     'verification_code': uuid.uuid4(),
#                     'code': uuid.uuid4().hex[:8]  # Generate or use existing code as needed
#                 }
#             )
#         except MultipleObjectsReturned:
#             # If multiple certificates are found, get the first one or handle accordingly
#             certificate = Certificate.objects.filter(user=user_newuser, course=course).first()

#     else:
#         # Handle case for anonymous users
#         try:
#             certificate, created = Certificate.objects.get_or_create(
#                 course=course,
#                 defaults={
#                     'verification_code': uuid.uuid4(),
#                     'code': uuid.uuid4().hex[:8]  # Generate or use existing code as needed
#                 }
#             )
#         except MultipleObjectsReturned:
#             # If multiple certificates are found, get the first one or handle accordingly
#             certificate = Certificate.objects.filter(course=course).first()

#     # Get additional data required for rendering the PDF
#     student = Profile.objects.filter(user_id=request.user.id).first() if request.user.is_authenticated else None

#     date = timezone.now()
#     logo = Logo.objects.all()
#     sign = Signature.objects.all()
#     design = Designcert.objects.all()

#     # Context for rendering the PDF
#     context = {
#         # 'student':student,
#         'results': [course],
#         'first_name': certificate.user.first_name if certificate.user else 'Anonymous',
#         'last_name': certificate.user.last_name if certificate.user else '',
#         'date': date,
#         'course': [course],
#         'logo': logo,
#         'sign': sign,
#         'design': design,
#         'school_name': certificate.user.school.school_name if certificate.user and certificate.user.school else '',
#         'school_logo': certificate.user.school.logo if certificate.user and certificate.user.school else '',
#         'school_sign': certificate.user.school.principal_signature if certificate.user and certificate.user.school else '',
#         'principal_name': certificate.user.school.name if certificate.user and certificate.user.school else '',
#         'portfolio': certificate.user.school.portfolio if certificate.user and certificate.user.school else '',
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
