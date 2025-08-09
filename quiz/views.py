from django.conf import settings
from django.shortcuts import render

# Create your views here.
# topics assessment view 
from users.models import Profile
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Subquery, OuterRef
from quiz.models import TopicsAssessment, QuestionAssessment, ResultAssessment, Course
from django.http import HttpResponseRedirect
import openai

from .models import Topics, TopicsAssessment, QuestionAssessment
from django.contrib import messages


# views.py
from openai import OpenAI
import re

client = OpenAI(api_key=settings.OPENAI_API_KEY)

@login_required
def generate_ai_questions(request):
    assessments = TopicsAssessment.objects.select_related('course_name').all()

    # ✅ Handle confirm-save POST request
    if request.method == 'POST' and request.POST.get("confirm_save") == "1":
        total_questions = int(request.POST.get("total_questions"))
        assessment_id = request.POST.get("assessment_id")
        marks = int(request.POST.get("marks"))

        try:
            assessment = TopicsAssessment.objects.get(id=assessment_id)
        except TopicsAssessment.DoesNotExist:
            messages.error(request, "Invalid assessment.")
            return redirect('quiz:generate_ai_questions')

        saved = 0
        for i in range(1, total_questions + 1):
            question_text = request.POST.get(f"question_{i}", "").strip()
            option1 = request.POST.get(f"option1_{i}", "").strip()
            option2 = request.POST.get(f"option2_{i}", "").strip()
            option3 = request.POST.get(f"option3_{i}", "").strip()
            option4 = request.POST.get(f"option4_{i}", "").strip()
            answer = request.POST.get(f"answer_{i}", "Option1").strip()

            if question_text and option1 and option2 and option3 and option4:
                QuestionAssessment.objects.create(
                    course=assessment,
                    marks=marks,
                    question=question_text,
                    option1=option1,
                    option2=option2,
                    option3=option3,
                    option4=option4,
                    answer=answer
                )
                saved += 1

        messages.success(request, f"{saved} edited questions saved successfully.")
        return redirect('quiz:generate_ai_questions')

    # ✅ Initial generation POST request
    elif request.method == 'POST':
        assessment_id = request.POST.get('assessment')
        num_questions = int(request.POST.get('num_questions', 5))
        marks = int(request.POST.get('marks', 1))
        difficulty = request.POST.get('difficulty', 'medium').lower()  # 🔹 Read difficulty from form
        print("🛠 DEBUG — Selected difficulty:", difficulty)  # <-- Debug line

        try:
            assessment = TopicsAssessment.objects.get(id=assessment_id)
        except TopicsAssessment.DoesNotExist:
            messages.error(request, "Invalid assessment selected.")
            return redirect('quiz:generate_ai_questions')

        topic_title = assessment.course_name.courses.title

        def extract_subject_tag(topic_title):
            """Extracts the subject from a string like 'MATHS JSS2'."""
            return topic_title.split()[0].lower()

        subject_tag = extract_subject_tag(topic_title)
        topics = assessment.course_name

        # 🔹 Inject difficulty into the AI prompt
        if subject_tag in ['maths', 'mathematics', 'math', 'chemistry', 'chem', 'physics']:
            prompt = f"""Generate {num_questions} multiple-choice questions on the topic '{topics}' 
            at a {difficulty} difficulty level.
            Each question and its options must be strictly formatted using MathML with the namespace
            http://www.w3.org/1998/Math/MathML.

            Question: <math xmlns='http://www.w3.org/1998/Math/MathML'><mfrac><msup><mn>3</mn><mn>4</mn></msup><msup><mn>3</mn><mn>2</mn></msup></mfrac></math>?
            A. <math xmlns='http://www.w3.org/1998/Math/MathML'><mn>9</mn></math>
            B. <math xmlns='http://www.w3.org/1998/Math/MathML'><mn>6</mn></math>
            C. <math xmlns='http://www.w3.org/1998/Math/MathML'><mn>3</mn></math>
            D. <math xmlns='http://www.w3.org/1998/Math/MathML'><mn>27</mn></math>
            Answer: A
            """
        else:
            prompt = f"""You are an expert Python tutor.

            Generate {num_questions} {difficulty}-level multiple-choice Python questions 
            on the topic '{topic_title}'.
            Strictly follow this format (no explanations or extra text):

            Question: What is Python?
            A. A snake
            B. A type of car
            C. A programming language
            D. A fruit
            Answer: C

            Randomize correct answer position. Avoid repeating options or questions.
            """

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates programming quiz questions."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2000,
                temperature=0.7,
            )

            if not response.choices:
                messages.error(request, "OpenAI returned no content.")
                return redirect('quiz:generate_ai_questions')

            questions_text = response.choices[0].message.content.strip()
            blocks = re.split(r'\n\s*\n', questions_text.strip())

            preview_questions = []
            for block in blocks:
                lines = block.strip().split("\n")
                if len(lines) == 6:
                    question_text = lines[0].replace("Question:", "").strip()
                    options = [line.split('. ', 1)[1].strip() for line in lines[1:5]]
                    answer_letter = lines[5].split(':')[-1].strip().upper()

                    answer_map = {'A': 'Option1', 'B': 'Option2', 'C': 'Option3', 'D': 'Option4'}
                    answer = answer_map.get(answer_letter, 'Option1')

                    preview_questions.append({
                        'question': question_text,
                        'option1': options[0],
                        'option2': options[1],
                        'option3': options[2],
                        'option4': options[3],
                        'answer': answer
                    })
                else:
                    messages.warning(request, f"⚠️ Skipped malformed block:\n{block[:60]}...")

            return render(request, 'quiz/dashboard/generate_questions.html', {
                'assessments': assessments,
                'preview_questions': preview_questions,
                'assessment_id': assessment_id,
                'marks': marks,
            })

        except Exception as e:
            messages.error(request, f"OpenAI error: {str(e)}")
            return redirect('quiz:generate_ai_questions')

    # GET request
    return render(request, 'quiz/dashboard/generate_questions.html', {
        'assessments': assessments
    })


# @login_required
# def generate_ai_questions(request):
#     assessments = TopicsAssessment.objects.select_related('course_name').all()

#     # ✅ Handle confirm-save POST request
#     if request.method == 'POST' and request.POST.get("confirm_save") == "1":
#         total_questions = int(request.POST.get("total_questions"))
#         assessment_id = request.POST.get("assessment_id")
#         marks = int(request.POST.get("marks"))

#         try:
#             assessment = TopicsAssessment.objects.get(id=assessment_id)
#         except TopicsAssessment.DoesNotExist:
#             messages.error(request, "Invalid assessment.")
#             return redirect('quiz:generate_ai_questions')

#         saved = 0
#         for i in range(1, total_questions + 1):
#             question_text = request.POST.get(f"question_{i}", "").strip()
#             option1 = request.POST.get(f"option1_{i}", "").strip()
#             option2 = request.POST.get(f"option2_{i}", "").strip()
#             option3 = request.POST.get(f"option3_{i}", "").strip()
#             option4 = request.POST.get(f"option4_{i}", "").strip()
#             answer = request.POST.get(f"answer_{i}", "Option1").strip()

#             if question_text and option1 and option2 and option3 and option4:
#                 QuestionAssessment.objects.create(
#                     course=assessment,
#                     marks=marks,
#                     question=question_text,
#                     option1=option1,
#                     option2=option2,
#                     option3=option3,
#                     option4=option4,
#                     answer=answer
#                 )
#                 saved += 1

#         messages.success(request, f"{saved} edited questions saved successfully.")
#         return redirect('quiz:generate_ai_questions')

#     # ✅ Initial generation POST request
#     elif request.method == 'POST':
#         assessment_id = request.POST.get('assessment')
#         num_questions = int(request.POST.get('num_questions', 5))
#         marks = int(request.POST.get('marks', 1))

#         try:
#             assessment = TopicsAssessment.objects.get(id=assessment_id)
#         except TopicsAssessment.DoesNotExist:
#             messages.error(request, "Invalid assessment selected.")
#             return redirect('quiz:generate_ai_questions')
        
        
#         topic_title = assessment.course_name.courses.title
        
#         def extract_subject_tag(topic_title):
#             """Extracts the subject from a string like 'MATHS JSS2'."""
#             return topic_title.split()[0].lower()


#         # Format for Math, Chemistry, or Physics using MathML
#         subject_tag = extract_subject_tag(topic_title)
        
#         topics = assessment.course_name
#         # print("topics:", topics)

#         if subject_tag in ['maths', 'mathematics', 'math', 'chemistry', 'chem', 'physics']:
#             topics = assessment.course_name
#             prompt = f"""Generate {num_questions} multiple-choice questions on the topic '{topics}'.
#             Each question and its options must be strictly formatted using MathML with the namespace
#             http://www.w3.org/1998/Math/MathML. The question should be a math expression wrapped in <math> tags,
#             and each option should also be in MathML format.

#             Follow this exact structure:

#             Question: What is the value of <math xmlns='http://www.w3.org/1998/Math/MathML'><mfrac><msup><mn>3</mn><mn>4</mn></msup><msup><mn>3</mn><mn>2</mn></msup></mfrac></math>?
#             A. <math xmlns='http://www.w3.org/1998/Math/MathML'><mn>9</mn></math>
#             B. <math xmlns='http://www.w3.org/1998/Math/MathML'><mn>6</mn></math>
#             C. <math xmlns='http://www.w3.org/1998/Math/MathML'><mn>3</mn></math>
#             D. <math xmlns='http://www.w3.org/1998/Math/MathML'><mn>27</mn></math>
#             Answer: A
#             """
#         else:
#             prompt = f"""You are an expert Python tutor.

#             Generate {num_questions} multiple-choice Python questions on the topic '{topic_title}'.
#             Strictly follow this format (no explanations or extra text):

#             Question: What is Python?
#             A. A snake
#             B. A type of car
#             C. A programming language
#             D. A fruit
#             Answer: C

#             Randomize correct answer position. Avoid repeating options or questions.
#             """

#         try:
#             response = client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant that generates programming quiz questions."},
#                     {"role": "user", "content": prompt},
#                 ],
#                 max_tokens=2000,
#                 temperature=0.7,
#             )

#             if not response.choices:
#                 messages.error(request, "OpenAI returned no content.")
#                 return redirect('quiz:generate_ai_questions')

#             questions_text = response.choices[0].message.content.strip()
#             blocks = re.split(r'\n\s*\n', questions_text.strip())

#             preview_questions = []

#             for block in blocks:
#                 lines = block.strip().split("\n")
#                 if len(lines) == 6:
#                     question_text = lines[0].replace("Question:", "").strip()
#                     options = [line.split('. ', 1)[1].strip() for line in lines[1:5]]
#                     answer_letter = lines[5].split(':')[-1].strip().upper()

#                     answer_map = {'A': 'Option1', 'B': 'Option2', 'C': 'Option3', 'D': 'Option4'}
#                     answer = answer_map.get(answer_letter, 'Option1')

#                     preview_questions.append({
#                         'question': question_text,
#                         'option1': options[0],
#                         'option2': options[1],
#                         'option3': options[2],
#                         'option4': options[3],
#                         'answer': answer
#                     })
#                 else:
#                     messages.warning(request, f"⚠️ Skipped malformed block:\n{block[:60]}...")

#             return render(request, 'quiz/dashboard/generate_questions.html', {
#                 'assessments': assessments,
#                 'preview_questions': preview_questions,
#                 'assessment_id': assessment_id,
#                 'marks': marks,
#             })

#         except Exception as e:
#             messages.error(request, f"OpenAI error: {str(e)}")
#             return redirect('quiz:generate_ai_questions')

#     # GET request
#     return render(request, 'quiz/dashboard/generate_questions.html', {
#         'assessments': assessments
#     })



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
