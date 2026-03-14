

# Register your models heres.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import Profile, NewUser,BadgeDownload

from quiz.models import Course, Question, Result

# from django.contrib.auth import get_user_model
# User = get_user_model()

from import_export.admin import ImportExportModelAdmin
from import_export import fields,resources
from import_export.widgets import ForeignKeyWidget


# In admin.py

from django.contrib import admin
from .models import UserVisit, PageView

@admin.register(UserVisit)
class UserVisitAdmin(admin.ModelAdmin):
    list_display = ['user', 'visit_time', 'last_activity', 'duration_seconds', 'page_views', 'device_type', 'browser', 'ip_address']
    list_filter = ['visit_time', 'device_type', 'browser', 'os']
    search_fields = ['user__username', 'ip_address', 'entry_page']
    date_hierarchy = 'visit_time'
    readonly_fields = ['visit_time', 'last_activity', 'duration_seconds']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['visit', 'url', 'timestamp', 'time_on_page']
    list_filter = ['timestamp']
    search_fields = ['url', 'title']
    date_hierarchy = 'timestamp'
    readonly_fields = ['timestamp']

admin.site.register(BadgeDownload)


class NewUserResource(resources.ModelResource):
    
    class Meta:
        model = NewUser
               
class NewUserAdmin(ImportExportModelAdmin):
    list_display = ['id', 'email', 'username', 'phone_number', 'first_name', 'last_name', 'student_class', 'school', 'countries', 'is_staff', 'is_superuser', 'is_active', 'last_login', 'date_joined']
    list_filter = ['email', 'username', 'school', 'phone_number', 'first_name', 'last_login', 'student_class']
    search_fields = ['email', 'username', 'school__school_name', 'phone_number', 'first_name', 'last_login', 'student_class']  # Use school__name to search by school name
    ordering = ['date_joined']
    
    resource_class = NewUserResource

admin.site.register(NewUser, NewUserAdmin)


class ProfileResource(resources.ModelResource):
    
    courses = fields.Field(
        column_name= 'user',
        attribute='user',
        widget=ForeignKeyWidget(NewUser,'email') )
    
    class Meta:
        model = Profile
        # fields = ('title',)
               
class ProfileAdmin(ImportExportModelAdmin):
    list_display = ['id', 'user','username', 'first_name', 'last_name','gender', 'phone_number', 'countries','pro_img', 'bio', 'created','updated']
    list_filter =  ['user','username', 'first_name', 'last_name','gender' ]
    search_fields = ['user__email','user__first_name','user__last_name', 'username', 'gender']
    ordering = ['created']
    
    resource_class = ProfileResource

admin.site.register(Profile, ProfileAdmin)


