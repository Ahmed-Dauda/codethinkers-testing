from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import Profile
from users.models import NewUser
from quiz.models import Course, Question, Result
# from student.models import Student
# from django.contrib.auth import get_user_model
# User = get_user_model()
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields,resources
from import_export.widgets import ForeignKeyWidget

# class UserAdmin(BaseUserAdmin):
#     fieldsets = (
#         (None, {'fields': ('email','username', 'password','countries', 'phone_number','last_login')}),
#         ('Permissions', {'fields': (
#             'is_active', 
#             'is_staff', 
#             'is_superuser',
#             'groups', 
#             'user_permissions',
#         )}),
#     )
#     add_fieldsets = (
#         (
#             None,
#             {
#                 'classes': ('wide',),
#                 'fields': ('username','first_name','last_name','email','countries','phone_number' ,'password1', 'password2')
#             }
#         ),
#     )

#     list_display = ('username','first_name','last_name', 'email','countries', 'phone_number', 'last_login')
#     list_filter = ( 'is_superuser', 'is_active', 'groups')
#     search_fields = ('email',)
#     ordering = ('email',)
#     filter_horizontal = ('groups', 'user_permissions',)

# admin.site.register(NewUser, UserAdmin)
# admin.site.register(Profile)



class NewUserResource(resources.ModelResource):
    
    # courses = fields.Field(
    #     column_name= 'user',
    #     attribute='user',
    #     widget=ForeignKeyWidget(NewUser,'username') )
    
    class Meta:
        model = NewUser
        # fields = ('title',)
               
class NewUserAdmin(ImportExportModelAdmin):
    list_display = ['id', 'email','username', 'phone_number', 'first_name', 'last_name','countries' ,'is_staff', 'is_superuser', 'is_active','last_login', 'date_joined']
    list_filter =  ['id', 'email','username', 'first_name', 'last_login']
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
    list_display = ['id', 'user','username', 'first_name', 'last_name', 'gender', 'phone_number', 'countries','pro_img', 'bio', 'created','updated']
    list_filter =  ['id', 'user','username', 'first_name', 'last_name', 'gender']
    search_fields = ['id', 'user','username', 'first_name', 'last_name', 'gender']
    ordering = ['id']
    
    resource_class = ProfileResource

admin.site.register(Profile, ProfileAdmin)


# class ProfileResource(resources.ModelResource):
    
#     courses = fields.Field(
#         column_name= 'user',
#         attribute='user',
#         widget=ForeignKeyWidget(NewUser,'username') )
    
#     class Meta:
#         model = Profile
#         # fields = ('title',)
               
# class ProfileAdmin(ImportExportModelAdmin):
#     list_display = ['id', 'user','username', 'first_name', 'last_name', 'gender', 'phone_number', 'countries', 'bio', 'created']
#     list_filter =  ['id', 'user','username', 'first_name', 'last_name', 'gender']
#     search_fields = ['id', 'user__username','username', 'first_name', 'last_name', 'gender']
#     ordering = ['id']
    
#     resource_class = ProfileResource

# admin.site.register(Profile, ProfileAdmin)

