# instructor/views.py
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from instructor.utils import split_commission
from sms.models import Courses

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from sms.models import Courses  # Main courses
from quiz.models import Course, TopicsAssessment   # Exam model
from instructor.models import InstructorEarning
from users.models import NewUser
from quiz.models import Course
from .forms import CourseQuizForm, QuestionAssessmentForm, TopicsAssessmentForm,TopicsForm

from sms.models import Topics

def add_topics_assessment(request):
    if request.method == 'POST':
        form = TopicsAssessmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('instructor:add_topics_assessment')
    else:
        form = TopicsAssessmentForm()

    assessments = TopicsAssessment.objects.select_related(
        'course_name'
    ).order_by('-created')

    topics = Topics.objects.all().order_by('title')

    return render(
        request,
        'instructor/add_topics_assessment.html',
        {
            'form': form,
            'assessments': assessments,
            'topics': topics,
        }
    )


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages


def delete_topics_assessment(request, assessment_id):
    assessment = get_object_or_404(TopicsAssessment, id=assessment_id)

    if request.method == 'POST':
        assessment.delete()
        messages.success(request, "Topic assessment deleted successfully.")
        return redirect('instructor:add_topics_assessment')  # Redirect back to the list

    return redirect('instructor:add_topics_assessment')  # fallback


@login_required
def add_topic(request):
    """
    Instructor adds a new topic to one of their courses.
    """
    if request.method == 'POST':
        form = TopicsForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            # Ensure the course belongs to this instructor
            if topic.courses.course_owner != request.user:
                form.add_error('courses', "You cannot add a topic to this course.")
            else:
                topic.save()
                return redirect('instructor:dashboard')
    else:
        form = TopicsForm()
        # Limit the courses dropdown to courses owned by this instructor
        form.fields['courses'].queryset = Courses.objects.filter(course_owner=request.user)

    return render(request, 'instructor/add_topic.html', {'form': form})


@login_required
def add_question_assessment(request):
    """
    Allows instructor to add a question to their own TopicsAssessment only.
    """
    if request.method == 'POST':
        form = QuestionAssessmentForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.cleaned_data['course']
            # Ensure the instructor owns the topic
            if topic.course_name.course_owner != request.user.email:
                form.add_error('course', "You cannot add questions to this topic.")
            else:
                form.save()
                return redirect('instructor:dashboard')
    else:
        form = QuestionAssessmentForm()
        # Limit dropdown to only the instructor's topics
        form.fields['course'].queryset = TopicsAssessment.objects.filter(
            course_name__courses__course_owner=request.user.email
        )

    return render(request, 'instructor/add_question_assessment.html', {
        'form': form
    })


# views.py


from django.db.models import Sum
from sms.models import Courses, Topics

@login_required
def instructor_dashboard(request):
    instructor = request.user

    # 🔹 Courses owned by instructor
    courses_qs = Courses.objects.filter(course_owner=instructor.email)

    course_data = []

    for course in courses_qs:

        # Course engagement
        hit_count = getattr(course, 'hit_count_generic', None)
        enrollment_count = getattr(course, 'students', None)

        # Earnings for this course
        earnings_qs = InstructorEarning.objects.filter(
            instructor=instructor,
            course=course
        )

        earnings_summary = earnings_qs.aggregate(
            total_sales=Sum('amount_paid'),
            instructor_earned=Sum('instructor_amount'),
            platform_cut=Sum('platform_amount'),
        )

        course_data.append({
            'id': course.id,
            'title': course.title,
            'slug': course.slug if hasattr(course, 'slug') else None,  # Add slug
            'course_type': course.course_type,
            'status_type': course.status_type,
            'price': course.price,
            'cert_price': course.cert_price,
            'hit_count': hit_count.count() if hit_count else 0,
            'enrollments': enrollment_count.count() if enrollment_count else 0,
            'total_sales': earnings_summary['total_sales'] or 0,
            'instructor_earned': earnings_summary['instructor_earned'] or 0,
            'platform_cut': earnings_summary['platform_cut'] or 0,
            'created': course.created,
            'updated': course.updated,
            'img_course': course.img_course,
            'course_logo': course.course_logo,
        })

    # 🔹 Overall instructor totals (ALL courses)
    totals = InstructorEarning.objects.filter(
        instructor=instructor
    ).aggregate(
        total_sales=Sum('amount_paid'),
        instructor_earned=Sum('instructor_amount'),
        platform_cut=Sum('platform_amount'),
    )

    totals = {k: v or 0 for k, v in totals.items()}

    # 🔹 Earnings history (transactions)
    earnings_list = InstructorEarning.objects.filter(
        instructor=instructor
    ).select_related(
        'course', 'payment', 'certificate_payment'
    ).order_by('-created')

    context = {
        'instructor': instructor,
        'courses': course_data,
        'earnings_list': earnings_list,
        'total_courses': courses_qs.count(),
        'last_activity': instructor.last_login,
        'totals': totals,
    }

    return render(request, 'instructor/dashboard.html', context)


@login_required
def instructor_course_topics(request, course_id):
    """View to display all topics for a specific course in instructor dashboard"""
    instructor = request.user
    
    # Get the course and verify ownership
    course = get_object_or_404(
        Courses, 
        id=course_id, 
        course_owner=instructor.email
    )
    
    # Get all topics for this course
    topics = Topics.objects.filter(courses=course).select_related(
        'categories'
    ).prefetch_related(
        'completed_by',
        'hit_count_generic'
    ).order_by('created')
    
    # Topic statistics
    topic_stats = []
    for topic in topics:
        hit_count = getattr(topic, 'hit_count_generic', None)
        completed_count = topic.completed_by.count() if hasattr(topic, 'completed_by') else 0
        
        topic_stats.append({
            'id': topic.id,
            'title': topic.title,
            'slug': topic.slug,
            'categories': topic.categories,
            'desc': topic.desc,
            'transcript': topic.transcript,
            'img_topic': topic.img_topic,
            'video': topic.video,
            'topics_url': topic.topics_url,
            'created': topic.created,
            'updated': topic.updated,
            'is_completed': topic.is_completed,
            'hit_count': hit_count.count() if hit_count else 0,
            'completed_count': completed_count,
        })
    
    # Course engagement
    course_hit_count = getattr(course, 'hit_count_generic', None)
    course_enrollment_count = getattr(course, 'students', None)
    
    # Course earnings
    earnings_summary = InstructorEarning.objects.filter(
        instructor=instructor,
        course=course
    ).aggregate(
        total_sales=Sum('amount_paid'),
        instructor_earned=Sum('instructor_amount'),
        platform_cut=Sum('platform_amount'),
    )
    
    context = {
        'instructor': instructor,
        'course': course,
        'topics': topic_stats,
        'total_topics': topics.count(),
        'course_hit_count': course_hit_count.count() if course_hit_count else 0,
        'course_enrollments': course_enrollment_count.count() if course_enrollment_count else 0,
        'earnings_summary': {k: v or 0 for k, v in earnings_summary.items()},
    }
    
    return render(request, 'instructor/course_topics.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from sms.models import Courses, Topics, Categories
from .forms import TopicForm  # We'll create this form below



@login_required
def add_topic(request, course_id):
    """Add a new topic to a course"""
    instructor = request.user
    
    # Get the course and verify ownership
    course = get_object_or_404(Courses, id=course_id, course_owner=instructor.email)
    
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.courses = course
            topic.save()
            
            messages.success(request, f'Topic "{topic.title}" added successfully!')
            return redirect('instructor:course_topics', course_id=course.id)
    else:
        form = TopicForm()
    
    context = {
        'form': form,
        'course': course,
        'page_title': 'Add New Topic',
    }
    
    return render(request, 'instructor/topic_form.html', context)


@login_required
def edit_topic(request, topic_id):
    """Edit an existing topic"""
    instructor = request.user
    
    # Get the topic and verify course ownership
    topic = get_object_or_404(Topics, id=topic_id)
    
    # Check if instructor owns the course
    if topic.courses.course_owner != instructor.email:
        messages.error(request, 'You do not have permission to edit this topic.')
        return HttpResponseForbidden("You don't have permission to edit this topic.")
    
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES, instance=topic)
        if form.is_valid():
            topic = form.save()
            
            messages.success(request, f'Topic "{topic.title}" updated successfully!')
            return redirect('instructor:course_topics', course_id=topic.courses.id)
    else:
        form = TopicForm(instance=topic)
    
    context = {
        'form': form,
        'course': topic.courses,
        'topic': topic,
        'page_title': 'Edit Topic',
    }
    
    return render(request, 'instructor/topic_form.html', context)


@login_required
def delete_topic(request, topic_id):
    """Delete a topic"""
    instructor = request.user
    
    # Get the topic and verify course ownership
    topic = get_object_or_404(Topics, id=topic_id)
    
    # Check if instructor owns the course
    if topic.courses.course_owner != instructor.email:
        messages.error(request, 'You do not have permission to delete this topic.')
        return HttpResponseForbidden("You don't have permission to delete this topic.")
    
    course_id = topic.courses.id
    topic_title = topic.title
    
    if request.method == 'POST':
        topic.delete()
        messages.success(request, f'Topic "{topic_title}" deleted successfully!')
        return redirect('instructor:course_topics', course_id=course_id)
    
    context = {
        'topic': topic,
        'course': topic.courses,
    }
    
    return render(request, 'instructor/topic_confirm_delete.html', context)



#working fine
# @login_required
# def instructor_dashboard(request):
#     instructor = request.user

#     # 🔹 Courses owned by instructor
#     courses_qs = Courses.objects.filter(course_owner=instructor.email)

#     course_data = []

#     for course in courses_qs:

#         # Course engagement
#         hit_count = getattr(course, 'hit_count_generic', None)
#         enrollment_count = getattr(course, 'students', None)

#         # Earnings for this course
#         earnings_qs = InstructorEarning.objects.filter(
#             instructor=instructor,
#             course=course
#         )

#         earnings_summary = earnings_qs.aggregate(
#             total_sales=Sum('amount_paid'),
#             instructor_earned=Sum('instructor_amount'),
#             platform_cut=Sum('platform_amount'),
#         )

#         course_data.append({
#             'id': course.id,
#             'title': course.title,
#             'course_type': course.course_type,
#             'status_type': course.status_type,
#             'price': course.price,
#             'cert_price': course.cert_price,
#             'hit_count': hit_count.count() if hit_count else 0,
#             'enrollments': enrollment_count.count() if enrollment_count else 0,
#             'total_sales': earnings_summary['total_sales'] or 0,
#             'instructor_earned': earnings_summary['instructor_earned'] or 0,
#             'platform_cut': earnings_summary['platform_cut'] or 0,
#             'created': course.created,
#             'updated': course.updated,
#             'img_course': course.img_course,
#             'course_logo': course.course_logo,
#         })

#     # 🔹 Overall instructor totals (ALL courses)
#     totals = InstructorEarning.objects.filter(
#         instructor=instructor
#     ).aggregate(
#         total_sales=Sum('amount_paid'),
#         instructor_earned=Sum('instructor_amount'),
#         platform_cut=Sum('platform_amount'),
#     )

#     totals = {k: v or 0 for k, v in totals.items()}

#     # 🔹 Earnings history (transactions)
#     earnings_list = InstructorEarning.objects.filter(
#         instructor=instructor
#     ).select_related(
#         'course', 'payment', 'certificate_payment'
#     ).order_by('-created')

#     context = {
#         'instructor': instructor,
#         'courses': course_data,
#         'earnings_list': earnings_list,
#         'total_courses': courses_qs.count(),
#         'last_activity': instructor.last_login,
#         'totals': totals,
#     }

#     return render(request, 'instructor/dashboard.html', context)


from django.db.models import Sum
from .models import InstructorEarning

@login_required
def instructor_earnings(request):
    earnings = InstructorEarning.objects.filter(
        instructor=request.user
    ).select_related('course')

    totals = earnings.aggregate(
        total_sales=Sum('amount_paid'),
        total_earned=Sum('instructor_amount'),
        platform_cut=Sum('platform_amount')
    )

    return render(request, 'instructor/earnings.html', {
        'earnings': earnings,
        'totals': totals
    })




# instructor/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CourseForm


@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)

            # 🔐 Set automatically (not from form)
            course.course_owner = request.user.email

            course.save()
            form.save_m2m()  # important for ManyToMany fields
            
            messages.success(request, 'Course created successfully')
            return redirect('instructor:add_course')
    else:
        form = CourseForm()

    return render(request, 'instructor/add_course.html', {
        'form': form
    })


@login_required
def edit_course(request, course_id):
    # ✅ Get the course and ensure the logged-in user owns it
    course = get_object_or_404(
        Courses,
        id=course_id,
        course_owner=request.user  # use User object, not email
    )

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            # ✅ Optional: add a success message
            from django.contrib import messages
            messages.success(request, "✅ Course updated successfully!")
            return redirect('instructor:dashboard')
    else:
        form = CourseForm(instance=course)

    return render(request, 'instructor/add_course.html', {
        'form': form,
        'edit': True
    })


@login_required
def delete_course(request, course_id):
    course = get_object_or_404(
        Courses,
        id=course_id,
        course_owner=request.user.email  # 🔒 ownership check
    )

    if request.method == "POST":
        course.delete()
        return redirect('instructor:dashboard')

    return render(request, 'instructor/confirm_delete.html', {'course': course})



@login_required
def course_exams(request, course_id):
    course = get_object_or_404(
        Courses,
        id=course_id,
        course_owner=request.user.email
    )

    exams = Course.objects.filter(course_name=course)

    context = {
        'course': course,
        'exams': exams,
    }
    return render(request, 'instructor/course_exams.html', context)


@login_required
def add_exam(request, course_id):
    course = get_object_or_404(
        Courses,
        id=course_id,
        course_owner=request.user.email
    )

    if request.method == 'POST':
        Course.objects.create(
            course_name=course,
            total_marks=request.POST.get('total_marks'),
            duration_minutes=request.POST.get('duration'),
            pass_mark=request.POST.get('pass_mark')
        )
        return redirect('instructor:course_exams', course_id=course.id)

    return render(request, 'instructor/add_exam.html', {'course': course})

@login_required
def edit_exam(request, exam_id):
    exam = get_object_or_404(Course, id=exam_id, course_name__course_owner=request.user.email)
    if request.method == 'POST':
        exam.total_marks = request.POST.get('total_marks')
        exam.show_questions = request.POST.get('show_questions')
        exam.duration_minutes = request.POST.get('duration')
        exam.pass_mark = request.POST.get('pass_mark')
        exam.full_screen = bool(request.POST.get('full_screen'))
        exam.save()
        return redirect('instructor:course_exams', course_id=exam.course_name.id)
    return render(request, 'instructor/edit_exam.html', {'exam': exam})

@login_required
def delete_exam(request, exam_id):
    exam = get_object_or_404(Course, id=exam_id, course_name__course_owner=request.user.email)
    course_id = exam.course_name.id
    exam.delete()
    return redirect('instructor:course_exams', course_id=course_id)