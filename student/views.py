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


# from pypaystack import Transaction, Customer, Plan



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
#         print("Referrer URL:", referrer)
#         print("amount:", paid_amount)

#         # Split the referrer URL by '/'
#         url_parts = referrer.split('/')
#         content_type = url_parts[-3]
#         print("content_type", content_type)
#         print('url:', url_parts[-3])
    

#         # Check if the last part of the URL is a numeric "id"
#         if url_parts[-2].isdigit():
#             id_value = url_parts[-2]
#             print("Extracted ID:", id_value)
#         else:
#             id_value = None

#         course = get_object_or_404(Courses, pk=id_value)
#         print("course printed:", course)
        
#         course_amount = course.price
      
#         if content_type == 'course':
#             payment = Payment.objects.create(
#                 ref=reference,
#                 amount=paid_amount,
#                 first_name=first_name,
#                 last_name=last_name,
#                 email=email,
#                 verified=verified,
#                 content_type = content_type
#             )
#             # Add courses to the payment using the 'set()' method
       
#             if course:
#                 payment.courses.set([course])
#                 payment.save()
               
#         course = get_object_or_404(Courses, pk=id_value)
        
#         if content_type == 'certificates':
#         # Create an instance of the CertificatePayment model
#             cert_payment = CertificatePayment(
#                 ref=reference,
#                 amount=paid_amount,
#                 first_name=first_name,
#                 last_name=last_name,
#                 email=email,
#                 verified=verified,
#                 content_type=content_type
#             )

#             # Check if the course exists (replace this with the actual condition)
#             if course:
#                 # Set courses for the CertificatePayment instance
#                 cert_payment.courses.set([course])
#                 cert_payment.save()

#             # Save the CertificatePayment instance to the database
#             cert_payment.save()


#         course = get_object_or_404(PDFDocument, pk=id_value)
#         if content_type == 'ebooks':
         
#             payment = EbooksPayment.objects.create(
#                 ref=reference,
#                 amount=paid_amount,
#                 first_name=first_name,
#                 last_name=last_name,
#                 email=email,
#                 verified=verified,
#                 content_type = course,
              
#             )
#             # print("", id_value)
#             # # course = get_object_or_404(PDFDocument, pk=id_value)
#             # print('pdfcourse', course)
#             # Add courses to the payment using the 'set()' method
#             # if course:
#             #     payment.courses.set([course])

#         return JsonResponse({'status': 'success'})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Unsupported event type'}, status=400)


@csrf_exempt
@require_POST
@transaction.non_atomic_requests(using='db_name')
def paystack_webhook(request):
    # ... (existing code)


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
        # first_name = request.user.profile.first_name
        # last_name = request.user.profile.last_name
        email = data['customer'].get('email')

        referrer = payload['data']['metadata']['referrer'].strip()
        print("Referrer URL:", referrer)
        print("amount:", paid_amount)

        # Split the referrer URL by '/'
        url_parts = referrer.split('/')
        content_type = url_parts[-3]
        print("content_type", content_type)
        print('url:', url_parts[-3])

        # Check if the last part of the URL is a numeric "id"
        if url_parts[-2].isdigit():
            id_value = url_parts[-2]
            print("Extracted ID:", id_value)
        else:
            id_value = None

        # Assuming 'Courses' is the model for certificates, adjust as needed
        course = get_object_or_404(QMODEL.Course, pk=id_value)
        print("course printed:", course)
        recode = get_object_or_404(NewUser, email = email)
        recode = recode.phone_number
        print("course printed: rrrrr", recode)

        # Check if a similar entry already exists
        existing_entry = CertificatePayment.objects.filter(
            ref=reference,
            amount=paid_amount,
            first_name=first_name,
            last_name=last_name,
            email=email,
            verified=verified,
            content_type=content_type,
            f_code = recode,
        ).first()
        if course:
                certpayment.courses.set([course.course_name])

        if existing_entry:
            # Skip the update step if no specific updates are needed
            pass
        else:
            # Create a new CertificatePayment instance
            certpayment = CertificatePayment.objects.create(
                ref=reference,
                amount=paid_amount,
                first_name=first_name,
                last_name=last_name,
                email=email,
                verified=verified,
                content_type=content_type,
                f_code = recode,
            )
            if course:
                certpayment.courses.set([course.course_name])


     
    # Adjust the model and field names accordingly
    # certpayment = CertificatePayment.objects.create(
    #     ref=reference,
    #     amount=paid_amount,
    #     first_name=first_name,
    #     last_name=last_name,
    #     email=email,
    #     verified=verified,
    #     content_type=content_type,
    # )

    # # Assuming 'courses' is the related name in CertificatePayment model, adjust as needed
    # if course:
    #     certpayment.courses.set([course.course_name])

    return JsonResponse({'status': 'success'})



# next for testing 

# end 

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
    course = QMODEL.Course.objects.get_queryset().order_by('id')
    context = {
        'courses':course
    }
    return render(request, 'student/dashboard/take_exams.html', context=context)

@login_required
def start_exams_view(request, pk):
    
    course = QMODEL.Course.objects.get(id = pk)
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




# def verify_cert(request):
#     certificate = get_object_or_404(Certificate, user=request.user)
#     # Perform any additional verification logic here

#     context = {
#         'certificate': certificate,
#     }
#     return render(request, 'student/verify_certificate.html', context)


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
    date = datetime.now()
    logo = Logo.objects.all() 
    sign = Signature.objects.all()  # Corrected import
    design = Designcert.objects.all()
    pk = kwargs.get('pk')
    posts = get_list_or_404(course, pk= pk)
    user_profile =  Profile.objects.filter(user_id = request.user)
    template_path = 'student/dashboard/certificatepdf.html'
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
    
