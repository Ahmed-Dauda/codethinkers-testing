from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import Profile, NewUser, Referrer

from quiz.models import Course, Question, Result

# from django.contrib.auth import get_user_model
# User = get_user_model()
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields,resources
from import_export.widgets import ForeignKeyWidget




class NewUserResource(resources.ModelResource):
    
    # courses = fields.Field(
    #     column_name= 'user',
    #     attribute='user',
    #     widget=ForeignKeyWidget(NewUser,'username') )
    
    class Meta:
        model = NewUser
        # fields = ('title',)
               
class NewUserAdmin(ImportExportModelAdmin):
    list_display = ['id', 'email','username','phone_number', 'first_name', 'last_name','countries' ,'is_staff', 'is_superuser', 'is_active','last_login', 'date_joined']
    list_filter =  ['id', 'email','username','first_name', 'last_login']
    search_fields = ['id', 'email','username', 'first_name', 'last_login']
    ordering = ['id']
    
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
    list_filter =  ['id', 'user','username', 'first_name', 'last_name','gender' ]
    search_fields = ['id', 'user__email','user__first_name','user__last_name', 'username', 'gender']
    ordering = ['id']
    
    resource_class = ProfileResource

admin.site.register(Profile, ProfileAdmin)



# class ReferrerResource(resources.ModelResource):
#     user = fields.Field(
#         column_name='user',
#         attribute='user',
#         widget=ForeignKeyWidget(NewUser, 'email')
#     )

#     class Meta:
#         model = ReferrerProfile


# class ReferrerAdmin(ImportExportModelAdmin):
#     list_display = ['id', 'user', 'referrer']
#     list_filter = ['id', 'user', 'referrer']
#     search_fields = ['id', 'user', 'referrer']
#     ordering = ['id']

#     resource_class = ReferrerResource

# admin.site.register(ReferrerProfile, ReferrerAdmin)
admin.site.register(Referrer)