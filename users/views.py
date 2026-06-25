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
from django.db.models import Count, Sum, Avg, Q
from django.db.models.functions import TruncDate, TruncHour
from datetime import timedelta
from .models import UserVisit, PageView

def dashboard_view(request):
    now = timezone.now()
    
    # Get filter params from GET request
    month = int(request.GET.get('month', now.month))
    year = int(request.GET.get('year', now.year))

    # === NEW: Visit Statistics ===
    
    # Total visits all time
    total_visits = UserVisit.objects.count()
    
    # Unique visitors all time
    unique_visitors = UserVisit.objects.values('user').distinct().count()
    
    # Today's visits
    today_visits = UserVisit.objects.filter(
        visit_time__date=now.date()
    ).count()
    
    # This month's visits
    month_visits = UserVisit.objects.filter(
        visit_time__year=year,
        visit_time__month=month
    ).count()
    
    # This year's visits
    year_visits = UserVisit.objects.filter(
        visit_time__year=year
    ).count()
    
    # Average session duration (in minutes)
    avg_session_duration = UserVisit.objects.filter(
        session_ended=True
    ).aggregate(
        avg_duration=Avg('duration_seconds')
    )['avg_duration'] or 0
    avg_session_duration = round(avg_session_duration / 60, 2)  # Convert to minutes
    
    # Average page views per session
    avg_page_views = UserVisit.objects.aggregate(
        avg_views=Avg('page_views')
    )['avg_views'] or 0
    avg_page_views = round(avg_page_views, 2)
    
    # Device breakdown
    device_stats = UserVisit.objects.values('device_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Browser breakdown
    browser_stats = UserVisit.objects.values('browser').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Most visited pages
    top_pages = PageView.objects.values('url').annotate(
        views=Count('id')
    ).order_by('-views')[:10]
    
    # Visits by hour (last 24 hours)
    visits_by_hour = UserVisit.objects.filter(
        visit_time__gte=now - timedelta(hours=24)
    ).annotate(
        hour=TruncHour('visit_time')
    ).values('hour').annotate(
        count=Count('id')
    ).order_by('hour')
    
    # Visits by day (last 30 days)
    visits_by_day = UserVisit.objects.filter(
        visit_time__gte=now - timedelta(days=30)
    ).annotate(
        day=TruncDate('visit_time')
    ).values('day').annotate(
        count=Count('id')
    ).order_by('day')
    
    # New vs returning visitors (this month)
    new_visitors_count = UserVisit.objects.filter(
        visit_time__year=year,
        visit_time__month=month,
        user__isnull=False
    ).values('user').annotate(
        visit_count=Count('id')
    ).filter(visit_count=1).count()
    
    returning_visitors_count = month_visits - new_visitors_count
    
    # Top referring sites
    top_referrers = UserVisit.objects.exclude(
        Q(referrer='') | Q(referrer__isnull=True)
    ).values('referrer').annotate(
        count=Count('id')
    ).order_by('-count')[:10]

    # === Certificate download stats ===
    course_downloads = (
        CertificateDownload.objects
        .values('certificate__title')
        .annotate(total_downloads=Count('id'))
        .order_by('-total_downloads')[:5]
    )

    # === Badge download stats ===
    from django.db.models import F
    courses = Course.objects.all()
    badge_downloads = []

    for course in courses:
        counts = BadgeDownload.objects.filter(course=course).aggregate(
            total_downloads=Count('id'),
            gold_downloads=Count('id', filter=Q(rank=1)),
            silver_downloads=Count('id', filter=Q(rank=2)),
            bronze_downloads=Count('id', filter=Q(rank=3)),
            participant_downloads=Count('id', filter=Q(rank__gt=3))
        )
        counts['course_name'] = course.course_name
        badge_downloads.append(counts)

    badge_downloads = sorted(badge_downloads, key=lambda x: x['total_downloads'], reverse=True)

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
        
        # ✅ NEW: Visit statistics
        "total_visits": total_visits,
        "unique_visitors": unique_visitors,
        "today_visits": today_visits,
        "month_visits": month_visits,
        "year_visits": year_visits,
        "avg_session_duration": avg_session_duration,
        "avg_page_views": avg_page_views,
        "device_stats": device_stats,
        "browser_stats": browser_stats,
        "top_pages": top_pages,
        "visits_by_hour": visits_by_hour,
        "visits_by_day": visits_by_day,
        "new_visitors_count": new_visitors_count,
        "returning_visitors_count": returning_visitors_count,
        "top_referrers": top_referrers,
    }

    return render(request, "users/quick_dashboard.html", context)

def visit_stats_api(request):
    """API endpoint for real-time visit statistics"""
    now = timezone.now()
    
    # Current active visitors (last 5 minutes)
    active_visitors = UserVisit.objects.filter(
        last_activity__gte=now - timedelta(minutes=5)
    ).count()
    
    # Today's stats
    today_stats = UserVisit.objects.filter(
        visit_time__date=now.date()
    ).aggregate(
        total_visits=Count('id'),
        total_page_views=Sum('page_views'),
        avg_duration=Avg('duration_seconds')
    )
    
    return JsonResponse({
        "active_visitors": active_visitors,
        "today_visits": today_stats['total_visits'] or 0,
        "today_page_views": today_stats['total_page_views'] or 0,
        "avg_duration_minutes": round((today_stats['avg_duration'] or 0) / 60, 2),
    })


def online_users_api(request):
    """API endpoint for real-time online users"""
    now = timezone.now()
    users = NewUser.objects.filter(last_activity__gte=now - timedelta(minutes=5))
    return JsonResponse({
        "users": list(users.values("username", "email"))
    })


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
