from django.urls import path
from .views import add_exam, add_question_assessment, add_topic, add_topics_assessment, course_exams, delete_exam, delete_topics_assessment, edit_exam, instructor_dashboard, add_course, edit_course, delete_course

app_name = 'instructor'

urlpatterns = [
    path('delete-assessment/<int:assessment_id>/', delete_topics_assessment, name='delete_topics_assessment'),
    path('topics-assessment/', add_topics_assessment, name='add_topics_assessment'),
    path('add-topic/', add_topic, name='add_topic'),

    path(
        'add-question/',
        add_question_assessment,
        name='add_question_assessment'
    ),
    path('exam/<int:exam_id>/edit/', edit_exam, name='edit_exam'),
    path('exam/<int:exam_id>/delete/', delete_exam, name='delete_exam'),
    path('course/<int:course_id>/exams/add/', add_exam, name='add_exam'),
    path('course/<int:course_id>/exams/', course_exams, name='course_exams'),
    path("dashboard/", instructor_dashboard, name="dashboard"),
path('courses/add/', add_course, name='add_course'),
    path("edit-course/<int:course_id>/", edit_course, name="edit_course"),
    path("delete-course/<int:course_id>/", delete_course, name="delete_course"),
]
