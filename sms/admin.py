from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields,resources
from import_export.widgets import ForeignKeyWidget
from django.utils.html import format_html  

from sms.models import (
    Categories, Courses, Topics, 
    Comment, Blog, Blogcomment,Alert, Gallery, 
    FrequentlyAskQuestions, Partners, CourseFrequentlyAskQuestions, Skillyouwillgain, 
    # CourseLearnerReviews, 
    Whatyouwilllearn, 
    CareerOpportunities, Whatyouwillbuild, 
    AboutCourseOwner, 
    CourseLearnerReviews,
    CompletedTopics
    )


admin.site.register(Gallery)
admin.site.register(FrequentlyAskQuestions)
admin.site.register(Partners)
admin.site.register(CourseFrequentlyAskQuestions)
admin.site.register(Skillyouwillgain)
admin.site.register(CourseLearnerReviews)
admin.site.register(Whatyouwilllearn)
admin.site.register(CareerOpportunities)
admin.site.register(Whatyouwillbuild)
admin.site.register(AboutCourseOwner)

@admin.register(CompletedTopics)
class CompletedTopicsAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "topic",
        "get_course",
    )

    list_select_related = (
        "user",
        "user__user",
        "topic",
        "topic__courses",
    )

    search_fields = (
        "user__user__username",
        "user__user__email",
        "topic__title",
        "topic__courses__title",
    )

    list_filter = (
        "topic__courses",
    )

    ordering = (
        "user__user__username",
    )

    autocomplete_fields = (
        "user",
        "topic",
    )

    def get_course(self, obj):
        return obj.topic.courses
    get_course.short_description = "Course"

# class ArticleAdminResource(resources.ModelResource):
    
#     class Meta:
#         model = Gallery
        # fields = ('title',)



class ArticleAdminResource(resources.ModelResource):
    
    class Meta:
        model = Blog
        # fields = ('title',)
               
class ArticleAdminAdmin(ImportExportModelAdmin):
    
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['id', 'title', 'desc', 'created']
    list_filter =  ['title']
    search_fields = ['author__user','title']
    ordering = ['id']
    
    resource_class = ArticleAdminResource

admin.site.register(Blog, ArticleAdminAdmin)



class FeedbackcommentResource(resources.ModelResource):
    
    class Meta:
        model = Comment
        # fields = ('title',)
               
class FeedbackcommentResourceAdmin(ImportExportModelAdmin):
    list_display = ['id', 'title', 'desc', 'created']
    list_filter =  ['title']
    search_fields= ['title']
    ordering = ['id']
    
    resource_class = FeedbackcommentResource

admin.site.register(Comment, FeedbackcommentResourceAdmin)


class CategoriesResource(resources.ModelResource):
    
    class Meta:
        model = Categories
        # fields = ('title',)
               
class CategoriesAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'desc', 'created']
    list_filter =  ['name']
    search_fields= ['name', 'desc']
    ordering = ['id']
    
    resource_class = CategoriesResource

admin.site.register(Categories, CategoriesAdmin)


class CategoriesResource(resources.ModelResource):
    
    courses = fields.Field(
        column_name= 'categories',
        attribute='categories',
        widget=ForeignKeyWidget(Categories,'name') )
    
    class Meta:
        model = Courses
        prepopulated_fields = {"slug": ("course_name",)}
        # fields = ('title',)
               
class CoursesAdmin(ImportExportModelAdmin):
    list_display = ['id', 'categories','title', 'desc', 'created']
    list_filter =  ['categories','title']
    search_fields = ['categories__name','title']
    ordering = ['id']
    
    resource_class = CategoriesResource

admin.site.register(Courses, CoursesAdmin)



class blogcommentResource(resources.ModelResource):
    
    class Meta:
        model = Blogcomment
        # fields = ('title',)
               
class blogcommentAdmin(ImportExportModelAdmin):
    list_display = ['id','post','name' ,'content']
     # prepopulated_fields = {"slug": ("title",)}
    list_filter =  ['post','created','name']
    search_fields= ['post','name']
    ordering = ['id']
    
    resource_class = blogcommentResource

admin.site.register(Blogcomment, blogcommentAdmin)
    
class TopicsResource(resources.ModelResource):

    courses = fields.Field(
        column_name='courses',
        attribute='courses',
        widget=ForeignKeyWidget(Courses, 'title'))

    class Meta:
        model = Topics
        # fields = ('title',)


class TopicsAdmin(ImportExportModelAdmin):
    list_display = [
        'id',
        'title',
        'courses',
        'categories',
        'img_topic',
        'video',
        'topics_url',
        'is_completed',
        'created'
    ]

    prepopulated_fields = {"slug": ("title",)}

    list_filter = [
        'categories',
        'courses',
        'is_completed',
        'created'
    ]

    search_fields = [
        'id',
        'title',
        'desc',
        'categories__name',
        'courses__title'
    ]

    ordering = ['id']
    resource_class = TopicsResource

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title',
                'slug',
                'categories',
                'courses',
                'desc',
                'transcript'
            )
        }),

        ('Media', {
            'fields': (
                'img_topic',
                'video',
                'topics_url'
            ),
            'classes': ('collapse',)
        }),

        ('Completion Status', {
            'fields': ('is_completed',),
            'classes': ('collapse',)
        })
    )

    # ✅ Show completion status with icon
    def is_completed(self, obj):
        if obj.is_completed:
            return format_html('<span style="color:green; font-size:16px;">✅</span>')
        return format_html('<span style="color:#ccc; font-size:16px;">⭕</span>')
    is_completed.short_description = 'Done'
    is_completed.admin_order_field = 'is_completed'

admin.site.register(Topics, TopicsAdmin)


# class TopicsAdmin(ImportExportModelAdmin):
#     list_display = ['id', 'categories', 'courses','title', 'desc', 'img_topic', 'video', 'topics_url', 'created', 'updated']
#     prepopulated_fields = {"slug": ("title",)}
#     list_filter = ['categories', 'courses', 'created']
#     search_fields = ['id', 'title', 'created', 'categories__name', 'courses__title']  # Use double underscore for related fields
#     ordering = ['id']
#     resource_class = TopicsResource

# admin.site.register(Topics, TopicsAdmin)



class AlertAdmin(ImportExportModelAdmin):
    list_display = ['id','title','content','created']

    list_filter =  ['title','content','created']
    search_fields= ['id','title','content','created']
    ordering = ['id']

admin.site.register(Alert, AlertAdmin)