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

def pdf_id_view(request, pk):
    # Ensure the course exists
    course = get_object_or_404(Course, pk=pk)
    certificate = None

    # Get or create the CourseCertificateCount record for tracking downloads
    course_cert_count, _ = CourseCertificateCount.objects.get_or_create(
        title=course.course_name
    )

    if request.user.is_authenticated:
        user_newuser, created = NewUser.objects.get_or_create(email=request.user.email)

        try:
            certificate, created = Certificate.objects.get_or_create(
                user=user_newuser,
                course=course,
                defaults={
                    'verification_code': uuid.uuid4(),
                    'code': uuid.uuid4().hex[:8]
                }
            )
        except MultipleObjectsReturned:
            certificate = Certificate.objects.filter(user=user_newuser, course=course).first()

        # Log the download for authenticated users
        CertificateDownload.objects.create(
            certificate=course_cert_count,  # <-- now using CourseCertificateCount
            user=request.user
        )

    else:
        try:
            certificate, created = Certificate.objects.get_or_create(
                course=course,
                defaults={
                    'verification_code': uuid.uuid4(),
                    'code': uuid.uuid4().hex[:8]
                }
            )
        except MultipleObjectsReturned:
            certificate = Certificate.objects.filter(course=course).first()

        # Optional: log anonymous download
        CertificateDownload.objects.create(
            certificate=course_cert_count,  # <-- now using CourseCertificateCount
            user=None
        )

    # Extra data for PDF
    student = Profile.objects.filter(user_id=request.user.id).first() if request.user.is_authenticated else None
    date = timezone.now()
    logo = Logo.objects.all()
    sign = Signature.objects.all()
    design = Designcert.objects.all()

    context = {
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

    # Render PDF
    template_path = 'student/dashboard/certificatepdf_testing.html'
    template = get_template(template_path)
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="certificate.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse(f'We had some errors <pre>{html}</pre>', status=500)

    return response


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
