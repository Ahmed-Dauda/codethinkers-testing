from django.shortcuts import render

# Create your views here.
# topics assessment view 
from users.models import Profile
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Subquery, OuterRef
from quiz.models import TopicsAssessment, QuestionAssessment, ResultAssessment
from django.http import HttpResponseRedirect

@login_required
def take_exams_view(request):
    course = TopicsAssessment.objects.get_queryset().order_by('id')
    print("Course Title:", course.title)
    for ta in TopicsAssessment.objects.all():
        print("TopicsAssessment Course Name Title:", ta.course_name.title)
        print("TopicsAssessment topic Name:", ta.course_name)
    context = {
        'courses':course,
        'courses_title':ta.course_name.title,
        'courses_name':ta.course_name
    }
    return render(request, 'quiz/dashboard/take_exams.html', context=context)

from sms.models import Topics, Courses
from django.shortcuts import redirect, render, get_object_or_404
from urllib.parse import unquote
from string import ascii_uppercase  # Import uppercase letters



from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse



@login_required
def start_exams_view(request, pk):
    
    course = TopicsAssessment.objects.get(id = pk)
    questions = QuestionAssessment.objects.filter(course = course).order_by('id')
    topics = Topics.objects.all()
    q_count = QuestionAssessment.objects.all().filter(course = course).count()
    student = request.user.profile
    results = ResultAssessment.objects.filter(exam = course, student = student).order_by('id')
    paginator = Paginator(questions, 20) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    letters = list(ascii_uppercase)

    context = {
        'course':course,
        'questions':questions,
        'q_count':q_count,
        'page_obj':page_obj,
        'results':results,
        'letters':letters
      
    }
    if request.method == 'POST':
        pass
    response = render(request, 'quiz/dashboard/start_exams.html', context=context)
    response.set_cookie('course_id', course.id)
    return response
     
# end of dashboard view


from django.urls import reverse

@login_required
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course= TopicsAssessment.objects.get(id=course_id)
        
        total_marks=0
        questions= QuestionAssessment.objects.get_queryset().filter(course=course).order_by('id')
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = Profile.objects.get(user_id=request.user.id)
        result =ResultAssessment()
        
        result.marks=total_marks 
        result.exam=course
        result.student=student
        m = ResultAssessment.objects.aggregate(Max('marks'))
        max_q = ResultAssessment.objects.filter(student_id = OuterRef('student_id'),exam_id = OuterRef('exam_id'),).order_by('-marks').values('id')
        max_result = ResultAssessment.objects.filter(id__in = Subquery(max_q[:1]), exam=course, student=student)
        score = 0
        for max_value in max_result:
            score = score + max_value.marks
            
        if total_marks > score:
            result.save()
            

        return HttpResponseRedirect(reverse('quiz:start-exam', kwargs={'pk': course.pk}))
    else:
        return HttpResponseRedirect('take-exam')


@login_required
def view_result_view(request):
    courses= TopicsAssessment.objects.get_queryset().order_by('id')
    return render(request,'quiz/dashboard/view_result.html',{'courses':courses})


from django.db.models import Count

@login_required
def check_marks_view(request,pk):
    course= TopicsAssessment.objects.get(id=pk)
    student = Profile.objects.get_queryset().order_by('id')
 
    context = {
        'results':student,
        'course':course,
        'st':request.user,
        
    }
    return render(request,'quiz/dashboard/check_marks.html', context)


# end

