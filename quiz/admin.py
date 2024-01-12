import profile
from django.contrib import admin
from quiz.models import Certificate_note

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields,resources
from import_export.widgets import ForeignKeyWidget
from users.models import Profile
from quiz.models import (
    Question, Course, Result,
    QuestionAssessment, TopicsAssessment, ResultAssessment, School
   
    )
# Register your models here.
admin.site.register(Course)
admin.site.register(School)
admin.site.register(TopicsAssessment)
# admin.site.register(QuestionAssessment)

# QuestionAssessment

class QuestionAssessmentResource(resources.ModelResource):
    
    course = fields.Field(
        column_name= 'course',
        attribute='course',
        widget=ForeignKeyWidget(Course, field='course_name__title'))
    
    class Meta:
        model = QuestionAssessment
        # fields = ('title',)
               
class QuestionAssessmentAdmin(ImportExportModelAdmin):
    list_display = ['id','course','marks' ,'question']
    # prepopulated_fields = {"slug": ("title",)}
    list_filter =  ['course','marks' ,'question']
    search_fields= ['id','course__course_name__title','marks' ,'question']
    ordering = ['id']
    
    resource_class = QuestionAssessmentResource

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
    
    courses = fields.Field(
        column_name= 'student',
        attribute='student',
        widget=ForeignKeyWidget(Profile,'username') )
    
    class Meta:
        model = Result
        # fields = ('title',)
               
class ResultAdmin(ImportExportModelAdmin):
    list_display = ['id', 'student', 'exam', 'marks', 'created']
    list_filter = ['id', 'student', 'exam', 'marks']
    search_fields = ['id', 'student__first_name', 'student__last_name', 'exam__course_name__title', 'marks', 'created']
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
    list_display = ['id','course','marks' ,'question']
    # prepopulated_fields = {"slug": ("title",)}
    list_filter =  ['course','marks' ,'question']
    search_fields= ['id','course__course_name__title','marks' ,'question']
    ordering = ['id']
    
    resource_class = CourseResource

admin.site.register(Question, CourseAdmin)