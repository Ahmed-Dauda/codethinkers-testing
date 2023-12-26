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


# views.py

# from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
# from .forms import ReferrerSignupForm
# from .models import ReferrerProfile

# views.py

from django.shortcuts import render, redirect
from allauth.account.views import SignupView
from .forms import SimpleSignupForm


# views.py

# from allauth.account.views import SignupView
# from .forms import ReferrerSignupForm

# class ReferrerSignupView(SignupView):
#     template_name = 'users/registration/register_user.html'  # Update with your template path
#     form_class = ReferrerSignupForm

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         # Your additional logic after a successful signup
#         return response

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Add any additional context data you need
#         return context





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
