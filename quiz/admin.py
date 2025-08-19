import profile
from django.contrib import admin
from quiz.models import Certificate_note
from django.utils.html import strip_tags
from django.utils.text import Truncator
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields,resources
from import_export.widgets import ForeignKeyWidget
from users.models import Profile
from quiz.models import (
    Question, Course, Result,Topics,ExamType, Session, Term,
    QuestionAssessment, TopicsAssessment, ResultAssessment, School
   
    )
# Register your models here.
# admin.site.register(Course)
admin.site.register(School)
# admin.site.register(Session)
# admin.site.register(ExamType)
# admin.site.register(Term)

# admin.site.register(TopicsAssessment)
class TopicsAssessmentAdmin(admin.ModelAdmin):
    autocomplete_fields = ['course_name']
    search_fields = ['course_name__title']  # Adjust 'title' if your Topics model uses a different field
    list_display = ['course_name', 'question_number', 'total_marks', 'pass_mark', 'created']  # Optional

admin.site.register(TopicsAssessment, TopicsAssessmentAdmin)


class CourseAdmin(admin.ModelAdmin):    
    list_display = ['show_questions','categories', 'course_name','question_number', 'total_marks', 'pass_mark','num_attemps', 'duration_minutes', 'created']
    search_fields = ['course_name__title', 'schools__school_name']  # Add search field for course name and school name
    # autocomplete_fields = ['schools']
    # actions = [delete_unused_placeholder_courses]
    
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('schools', 'course_name')

    def get_school_name(self, obj):
        return obj.schools.school_name if obj.schools else "Enable Exam"
    get_school_name.short_description = 'School Name'

admin.site.register(Course, CourseAdmin)


# QuestionAssessment
class MatchOnlyExistingTopicsAssessmentWidget(ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        try:
            # Get existing topic
            topic = Topics.objects.get(title=value)
        except Topics.DoesNotExist:
            raise ValueError(f"No existing Topics found with title = '{value}'")

        try:
            # Get existing assessment for that topic
            return TopicsAssessment.objects.get(course_name=topic)
        except TopicsAssessment.DoesNotExist:
            raise ValueError(f"No TopicsAssessment linked to Topics.title = '{value}'")


# Resource for importing QuestionAssessment
class QuestionAssessmentResource(resources.ModelResource):
    course = fields.Field(
        column_name='course',
        attribute='course',
        widget=MatchOnlyExistingTopicsAssessmentWidget(TopicsAssessment, 'course_name')
    )

    question = fields.Field()
    option1 = fields.Field()
    option2 = fields.Field()
    option3 = fields.Field()
    option4 = fields.Field()

    def dehydrate_question(self, obj):
        return strip_tags(obj.question or '')

    def dehydrate_option1(self, obj):
        return strip_tags(obj.option1 or '')

    def dehydrate_option2(self, obj):
        return strip_tags(obj.option2 or '')

    def dehydrate_option3(self, obj):
        return strip_tags(obj.option3 or '')

    def dehydrate_option4(self, obj):
        return strip_tags(obj.option4 or '')

    class Meta:
        model = QuestionAssessment
        import_id_fields = ['id']
        fields = (
            'course',
            'marks',
            'question',
            'img_quiz',
            'option1',
            'option2',
            'option3',
            'option4',
            'answer',
            'created',
            'updated',
            'id',
        )


# Admin for QuestionAssessment with import-export
class QuestionAssessmentAdmin(ImportExportModelAdmin):
    list_display = [
        'id',
        'course',
        'marks',
        'short_question',
        'short_option1',
        'short_option2',
        'short_option3',
        'short_option4',
        'answer',
        'created',
        'updated',
    ]
    autocomplete_fields = ['course']
    list_filter = ['course', 'marks', 'answer']
    search_fields = ['id', 'course__course_name__title', 'question', 'option1', 'option2']
    ordering = ['id']
    resource_class = QuestionAssessmentResource

    

    def short_question(self, obj):
        return Truncator(strip_tags(obj.question)).chars(40)
    short_question.short_description = 'Question'

    def short_option1(self, obj):
        return Truncator(strip_tags(obj.option1)).chars(30)
    short_option1.short_description = 'Option 1'

    def short_option2(self, obj):
        return Truncator(strip_tags(obj.option2)).chars(30)
    short_option2.short_description = 'Option 2'

    def short_option3(self, obj):
        return Truncator(strip_tags(obj.option3)).chars(30)
    short_option3.short_description = 'Option 3'

    def short_option4(self, obj):
        return Truncator(strip_tags(obj.option4)).chars(30)
    short_option4.short_description = 'Option 4'

admin.site.register(QuestionAssessment, QuestionAssessmentAdmin)

# ENDQUESTIONASSESSMENT


class ResultAssessmentResource(resources.ModelResource):
    
    courses = fields.Field(
        column_name= 'student',
        attribute='student',
        widget=ForeignKeyWidget(Profile,'username') )
    
    class Meta:
        model = Result
        # fields = ('title',)
  
class ResultAssessmentAdmin(ImportExportModelAdmin):
    list_display = ['id', 'student', 'exam', 'marks', 'created']
    list_filter = ['id', 'student', 'exam', 'marks']
    search_fields = ['id', 'student__first_name', 'student__last_name', 'exam__course_name__title', 'marks', 'created']
    ordering = ['id']
    resource_class = ResultAssessmentResource

admin.site.register(ResultAssessment, ResultAssessmentAdmin)


class ResultResource(resources.ModelResource):
    exam_course_name = fields.Field(
        column_name='exam',
        attribute='exam__course_name__title'  
    )
    
    student_username = fields.Field(
        column_name='student_username',
        attribute='student__user__username',
    )

    student_first_name = fields.Field(
        column_name='student_first_name',
        attribute='student__first_name',
    )

    student_last_name = fields.Field(
        column_name='student_last_name',
        attribute='student__last_name',
    )
    
    class Meta:
        model = Result
        fields = ('id', 'exam_course_name', 'student_username', 'student_first_name', 'student_last_name', 'marks', 'created')

               
class ResultAdmin(ImportExportModelAdmin):
    list_display = ['id', 'student', 'exam', 'marks', 'created']
    list_filter = ['id', 'student', 'exam', 'marks']
    search_fields = ['student__first_name', 'student__last_name', 'exam__course_name__title', 'marks', 'created']
    ordering = ['id']
    resource_class = ResultResource

admin.site.register(Result, ResultAdmin)

 

class CertificateResource(resources.ModelResource):
    
    # course = fields.Field(
    #     column_name= 'course',
    #     attribute='course',
    #     widget=ForeignKeyWidget(Course,'course_name') )
    
    class Meta:
        model = Certificate_note
        # fields = ('title',)
               
class CertificateAdmin(ImportExportModelAdmin):
    list_display = ['id','note']
    
    list_filter =  ['note']
    search_fields= ['note']
    ordering = ['id']
    
    resource_class = CertificateResource

admin.site.register(Certificate_note, CertificateAdmin)


class CourseResource(resources.ModelResource):
    
    course = fields.Field(
        column_name= 'course',
        attribute='course',
        widget=ForeignKeyWidget(Course, field='course_name__title'))
    
    class Meta:
        model = Question
        # fields = ('title',)
               
class CourseAdmin(ImportExportModelAdmin):
    list_display = [
    'course','marks','question','img_quiz','option1','option2','option3','option4','answer','created','updated',
    ]
    # prepopulated_fields = {"slug": ("title",)}
    list_filter =  ['course','marks' ,'question']
    search_fields= ['course__course_name__title','marks' ,'question']
    ordering = ['id']

    
    resource_class = CourseResource

admin.site.register(Question, CourseAdmin)


