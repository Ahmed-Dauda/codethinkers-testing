from django.db.models.aggregates import Count
from django.shortcuts import render,redirect,reverse
from . import models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from teacher import models as TMODEL
# from student.models import  Student
from users.models import NewUser
from users.models import Profile
from allauth.account.views import SignupView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# views.py

from django.shortcuts import render, redirect
from allauth.account.views import SignupView
from .forms import SimpleSignupForm, SchoolStudentSignupForm
from django.http import HttpResponse

from allauth.account.utils import perform_login
from allauth.socialaccount import signals
from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.models import SocialAccount
from allauth.account import app_settings
# users/views.py
from django.shortcuts import render, redirect
from .forms import ReferrerMentorForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from allauth.account.views import SignupView
from .forms import SimpleSignupForm
 

from django.db.models import Count, Avg
from quiz.models import Course, Result, School, NewUser

from django.utils.timezone import datetime
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import NewUser

from django.db.models import Avg, Count
from datetime import datetime
from certificate_stats.models import CertificateDownload  # adjust to your app path

from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import now
from student.models import Payment, PDFDocument, DocPayment, CertificatePayment, EbooksPayment
from django.db.models import Count
from .models import BadgeDownload

# Total downloads for a specific course
# course_downloads = BadgeDownload.objects.filter(course=course).count()

# # Total downloads by rank for a course
# downloads_by_rank = (
#     BadgeDownload.objects.filter(course=course)
#     .values('rank')
#     .annotate(total=Count('id'))
# )


# def dashboard_view(request):
#     now = timezone.now()
    
#     # Get filter params from GET request
#     month = request.GET.get('month', now.month)
#     year = request.GET.get('year', now.year)

#     # Ensure month/year are integers
#     month = int(month)
#     year = int(year)

#     # === Course download stats ===
#     course_downloads = (
#         CertificateDownload.objects
#         .values('certificate__title')
#         .annotate(total_downloads=Count('id'))
#         .order_by('-total_downloads')[:5]
#     )

#     # === Online users in last 5 mins ===
#     online_users = NewUser.objects.filter(
#         last_activity__gte=now - timedelta(minutes=5)
#     )

#     # Helper to calculate totals
#     def calc_totals(model):
#         all_time = model.objects.aggregate(
#             total_amount=Sum('amount') or 0,
#             total_count=Count('id')
#         )
#         month_total = model.objects.filter(
#             date_created__year=year, date_created__month=month
#         ).aggregate(total=Sum('amount'))['total'] or 0
#         year_total = model.objects.filter(
#             date_created__year=year
#         ).aggregate(total=Sum('amount'))['total'] or 0
#         return {
#             'all_time_amount': all_time['total_amount'] or 0,
#             'all_time_count': all_time['total_count'],
#             'month_total': month_total,
#             'year_total': year_total
#         }

#     payment_stats = {
#         "general": calc_totals(Payment),
#         "ebooks": calc_totals(EbooksPayment),
#         "certificates": calc_totals(CertificatePayment),
#         "documents": calc_totals(DocPayment),
#     }

#     # Total for month/year
#     total_month = sum([p['month_total'] for p in payment_stats.values()])
#     total_year = sum([p['year_total'] for p in payment_stats.values()])

#     context = {
#         "total_students": NewUser.objects.filter(is_staff=False).count(),
#         "total_courses": Course.objects.count(),
#         "quizzes_today": Result.objects.filter(created__date=now.date()).count(),
#         "avg_score": Result.objects.aggregate(Avg('marks'))['marks__avg'],
#         "active_schools": School.objects.count(),
#         "top_students": (
#             Result.objects
#             .values('student__username')
#             .annotate(avg_score=Avg('marks'))
#             .order_by('-avg_score')[:5]
#         ),
#         "course_downloads": course_downloads,
#         "online_users": online_users,
#         "payment_stats": payment_stats,
#         "total_month": total_month,
#         "total_year": total_year,
#         "selected_month": month,
#         "selected_year": year,
#     }

#     return render(request, "users/quick_dashboard.html", context)

from django.db.models import Q, Count, Sum, Avg

def dashboard_view(request):
    now = timezone.now()
    
    # Get filter params from GET request
    month = int(request.GET.get('month', now.month))
    year = int(request.GET.get('year', now.year))

    # === Certificate download stats ===
    course_downloads = (
        CertificateDownload.objects
        .values('certificate__title')
        .annotate(total_downloads=Count('id'))
        .order_by('-total_downloads')[:5]
    )

    # === Badge download stats ===
    badge_downloads = (
        BadgeDownload.objects
        .values('course__title')
        .annotate(
            total_downloads=Count('id'),
            gold_downloads=Count('id', filter=Q(rank=1)),
            silver_downloads=Count('id', filter=Q(rank=2)),
            bronze_downloads=Count('id', filter=Q(rank=3)),
            participant_downloads=Count('id', filter=Q(rank__gt=3)),
        )
        .order_by('-total_downloads')[:5]
    )

    # === Online users in last 5 mins ===
    online_users = NewUser.objects.filter(
        last_activity__gte=now - timedelta(minutes=5)
    )

    # Helper to calculate totals
    def calc_totals(model):
        all_time = model.objects.aggregate(
            total_amount=Sum('amount') or 0,
            total_count=Count('id')
        )
        month_total = model.objects.filter(
            date_created__year=year, date_created__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0
        year_total = model.objects.filter(
            date_created__year=year
        ).aggregate(total=Sum('amount'))['total'] or 0
        return {
            'all_time_amount': all_time['total_amount'] or 0,
            'all_time_count': all_time['total_count'],
            'month_total': month_total,
            'year_total': year_total
        }

    payment_stats = {
        "general": calc_totals(Payment),
        "ebooks": calc_totals(EbooksPayment),
        "certificates": calc_totals(CertificatePayment),
        "documents": calc_totals(DocPayment),
    }

    # Total for month/year
    total_month = sum([p['month_total'] for p in payment_stats.values()])
    total_year = sum([p['year_total'] for p in payment_stats.values()])

    # Top students
    top_students = (
        Result.objects
        .values('student__username')
        .annotate(avg_score=Avg('marks'))
        .order_by('-avg_score')[:5]
    )

    context = {
        "total_students": NewUser.objects.filter(is_staff=False).count(),
        "total_courses": Course.objects.count(),
        "quizzes_today": Result.objects.filter(created__date=now.date()).count(),
        "avg_score": Result.objects.aggregate(Avg('marks'))['marks__avg'],
        "active_schools": School.objects.count(),
        "top_students": top_students,
        "course_downloads": course_downloads,
        "badge_downloads": badge_downloads,
        "online_users": online_users,
        "payment_stats": payment_stats,
        "total_month": total_month,
        "total_year": total_year,
        "selected_month": month,
        "selected_year": year,
    }

    return render(request, "users/quick_dashboard.html", context)



def online_users_api(request):
    now = timezone.now()
    users = NewUser.objects.filter(last_activity__gte=now - timedelta(minutes=5))
    return JsonResponse({"users": list(users.values("username", "email"))})




def SchoolStudentView(request):
    if request.method == 'POST':

        form = SchoolStudentSignupForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('sms:myprofile')  # Redirect to a success page
    else:
        form = SchoolStudentSignupForm()

    return render(request, 'users/school_student.html', {'form': form})

from django.views.generic.edit import CreateView
from .forms import SchoolSignupForm  # Import your form
from quiz.models import School  # Import your model
from django.urls import reverse_lazy

class SchoolSignupView(CreateView):
    template_name = 'users/school_registration.html'
    form_class = SchoolSignupForm
    model = School  # Set the model attribute to specify the model to be used
    success_url = reverse_lazy('sms:myprofile')

    def get_queryset(self):
        # Return an empty queryset
        return School.objects.none()

    def form_valid(self, form):
        # Additional logic before saving the form data (if needed)
        # ...

        # Save the form data to the database
        response = super().form_valid(form)

        # Additional logic after saving the form data (if needed)
        # ...

        return response


from allauth.account.views import SignupView


class ReferralSignupView(SignupView):
    template_name = 'users/referrer.html'
    form_class = SimpleSignupForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        referral_code = self.kwargs.get('referrer_code', '')
        context['form'].fields['phone_number'].initial = referral_code
        context['referrer_code'] = self.request.resolver_match.kwargs.get('referrer_code', '')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        referral_code = form.cleaned_data.get('phone_number', '')

        # Associate referral code with the user
        user = self.request.user
        user.phone_number = referral_code
        user.save()

        return response
    
from django.utils.timezone import now

@login_required
def become_referrer(request):
    if request.method == 'POST':
        form = ReferrerMentorForm(request.POST, request=request)
        if form.is_valid():
            form.instance.referrer = request.user
            form.save()
            return redirect('sms:myprofile')
    else:
        form = ReferrerMentorForm(initial={'referrer': request.user.pk}, request=request)
        # Set timestamp for bot protection
        request.session['referrer_form_created_at'] = now().isoformat()

    return render(request, 'users/become_referrer.html', {'form': form})


# working
# @login_required
# def become_referrer(request):
#     if request.method == 'POST':
#         form = ReferrerMentorForm(request.POST)
#         if form.is_valid():
#             # Set the referrer field before saving
#             form.instance.referrer = request.user
#             form.save()
#             return redirect('sms:myprofile')
#     else:
#         form = ReferrerMentorForm(initial={'referrer': request.user.pk})

#     return render(request, 'users/become_referrer.html', {'form': form})



# def referral_signup(request, referrer_code):
#     # Your referral logic goes here
#     # You can use the referrer_code to identify the referrer and associate it with the signup process
#     # ...

#     return HttpResponse(f"Referral signup page for referrer {referrer_code}")



def take_exams_view(request):
    course = QMODEL.Course.objects.all()
    context = {
        'courses':course
    }
    return render(request, 'student/take_exams.html', context=context)

def start_exams_view(request, pk):

    course = QMODEL.Course.objects.get(id = pk)
    questions = QMODEL.Question.objects.all().filter(course = course)
    context = {
        'course':course,
        'questions':questions
    }
    if request.method == 'POST':
        pass
    response = render(request, 'student/start_exams.html', context=context)
    response.set_cookie('course_id', course.id)
    return response


def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.Course.objects.get(id=course_id)
        
        total_marks=0
        questions=QMODEL.Question.objects.all().filter(course=course)
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = Profile.objects.filter(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks=total_marks
        result.exam=course
        result.student=student
        result.save()

        return HttpResponseRedirect('view_result')
import itertools
def view_result_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/view_result.html',{'courses':courses})


from django.db.models import Count

def check_marks_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = Profile.objects.filter(user_id=request.user.id)
    res= QMODEL.Result.objects.values_list('marks', flat=True).order_by('-marks').distinct()
    stu= QMODEL.Result.objects.values('student','exam','marks').distinct()
    
    vr = QMODEL.Result.objects.values('marks', 'student').annotate(marks_count = Count('marks')).filter(marks_count__gt = 0)
        

    results= QMODEL.Result.objects.order_by('-marks').filter(exam=course).filter(student=student)[:3]
    context = {
        'results':results,
        'course':course,
        'st':request.user,
        'res':res,
        'stu':stu
    }
    return render(request,'student/check_marks.html', context)
