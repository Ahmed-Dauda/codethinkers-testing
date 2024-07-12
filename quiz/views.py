from django.shortcuts import render

# Create your views here.
# topics assessment view 
from users.models import Profile
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Subquery, OuterRef
from quiz.models import TopicsAssessment, QuestionAssessment, ResultAssessment, Course
from django.http import HttpResponseRedirect

@login_required
def take_exams_view(request):
    course = TopicsAssessment.objects.get_queryset().order_by('id')
    # print("Course Title:", course.title)
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
    paginator = Paginator(questions, 1000) # Show 25 contacts per page.
    paginator_comp = Paginator(questions, 1) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)
   
    page_obj_comp = paginator_comp.get_page(page_number)
    letters = list(ascii_uppercase)

    context = {
        'course':course,
        'questions':questions,
        'q_count':q_count,
        'page_obj':page_obj,
        'page_obj_comp':page_obj_comp,
        'results':results,
        'letters':letters,
        'completed':"letters",
      
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
        course = get_object_or_404(TopicsAssessment, id=course_id)
        options = []  # List to store the selected options
        total_marks = 0
        questions = QuestionAssessment.objects.filter(course=course).order_by('id')
        for i in range(len(questions)):
            selected_ans = request.POST.get(str(i+1))
            options.append(selected_ans)  # Add selected option to the list
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks += questions[i].marks

        student = get_object_or_404(Profile, user_id=request.user.id)

        # Check if the result already exists
        existing_result = ResultAssessment.objects.filter(marks=total_marks,student=student, exam=course).first()

        if existing_result:
            # Update the existing result
            existing_result.marks = total_marks
            existing_result.option = options  # Save selected options as a list
            existing_result.save()
            print(existing_result, 'updated result')
        else:
            # Create a new result
            result = ResultAssessment.objects.create(
                marks=total_marks,
                exam=course,
                student=student,
                option=options  # Save selected options as a list
            )
            print(result, 'new result')

     
        
        return HttpResponseRedirect(f'/quiz/start-exam/{course.pk}')
    else:
        return HttpResponseRedirect('/quiz/take-exam')
       
# @login_required
# def calculate_marks_view(request):
#     if request.COOKIES.get('course_id') is not None:
#         course_id = request.COOKIES.get('course_id')
#         course= TopicsAssessment.objects.get(id=course_id)
#         options = []  # List to store the selected options
#         total_marks=0
#         questions= QuestionAssessment.objects.get_queryset().filter(course=course).order_by('id')
#         for i in range(len(questions)):
            
#             # selected_ans = request.COOKIES.get(str(i+1))
#             selected_ans = request.POST.get(str(i+1))
#             options.append(selected_ans)  # Add selected option to the list
#             print("answers", selected_ans)
            
#             actual_answer = questions[i].answer
#             if selected_ans == actual_answer:
#                 total_marks = total_marks + questions[i].marks
#         student = Profile.objects.get(user_id=request.user.id)
        
#         result =ResultAssessment()
        
#         result.marks=total_marks 
#         result.exam=course
#         result.student=student
#         # options_str = ", ".join(str(option) if option is not None else "None" for option in options)
#         result.option = options  # Save selected options as a comma-separated string
        
#         print("result", result)
#         print("pass mar", course.pass_mark)
        
#         result.save()

#         return HttpResponseRedirect(reverse('quiz:start-exam', kwargs={'pk': course.pk}))
#     else:
#         return HttpResponseRedirect('take-exam')



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

# views.py

from django.shortcuts import render, redirect
# from .forms import StudentRegistrationForm

# def register_student(request):
#     if request.method == 'POST':
#         form = StudentRegistrationForm(request.user, request.POST)
#         if form.is_valid():
#             form.save()
#             # return redirect('quiz:school_dashboard')
#     else:
#         form = StudentRegistrationForm()

#     return render(request, 'quiz/dashboard/student_registration.html', {'form': form})


# def school_dashboard(request, pk):

#         # Example usage (in a view or wherever you generate the certificate)
#     course = Course.objects.get(pk=pk)  # Replace with the actual course instance
#     student = Student.objects.get(pk=pk)  # Replace with the actual student instance
#     # Get the relevant information for the certificate
#     student_info = course.get_student_info_for_certificate(student)

#     # Now you can use student_info in your certificate generation logic
#     if student_info:
#         school_name = student_info['school_name']
#         logo_url = student_info['logo_url']
#         signature_url = student_info['signature_url']
#         # Add more fields as needed
 
#     context = {
#         'course': course,
#         'student': student,
#         'student_info': student_info,
#     }
#     # context =  {
#     #     'school_name': school_name,
#     #     'logo_url': logo_url,
#     #     'signature_url': signature_url,
#     #     }

#     return render(request, 'quiz/dashboard/school_dashboard.html', context)
# from django.shortcuts import render
# from .models import Course
# from .models import Student

# from .models import Student

# def get_student_for_user(user):
#     try:
#         # Assuming there is a one-to-one relationship between User and Student
#         return Student.objects.get(user=user.profile)
#     except Student.DoesNotExist:
#         return None


# def school_dashboard(request, course_id):
#     # Assuming you have a function to get the current student based on the logged-in user
#     student = get_student_for_user(request.user)

#     if student:
#         course = get_object_or_404(Course, id=course_id)

#         # Get the relevant information for the certificate
#         student_info = course.get_student_info_for_certificate(student)

#         # Pass the information to the template
#         context = {
#             'course': course,
#             'student': student,
#             'student_info': student_info,
#         }

#         return render(request, 'quiz/dashboard/school_dashboard.html', context)
#     else:
#         # Handle the case where the user is not associated with a student
#         return render(request, 'error_template.html', {'error_message': 'User is not associated with a student'})
