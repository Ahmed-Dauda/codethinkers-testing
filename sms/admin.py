from django.contrib import admin
from sms.models import Categories, Courses, Topics, Comment
# Register your models here.

@admin.register(Comment)
class commentadmin(admin.ModelAdmin):
    # list_display = ['id', 'name', 'desc', 'created']
    list_filter = ordering = ['created']
    ordering = ['created']

@admin.register(Categories)
class categoriesadmin(admin.ModelAdmin):
    # list_display = ['id', 'name', 'desc', 'created']
    ordering = ['created']

@admin.register(Courses)
class coursesadmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'desc', 'created']
    ordering = ['created']

@admin.register(Topics)
class topicsadmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'desc', 'created']
    ordering = ['created']


# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# from .models import User
# from django.contrib.auth import get_user_model
# User = get_user_model()

# class UserAdmin(BaseUserAdmin):
#     fieldsets = (
#         (None, {'fields': ('email', 'password','country', 'last_login')}),
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
#                 'fields': ('first_name','first_name','email','country', 'password1', 'password2')
#             }
#         ),
#     )

#     list_display = ('first_name','first_name', 'email','country', 'is_staff', 'last_login')
#     list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
#     search_fields = ('email',)
#     ordering = ('email',)
#     filter_horizontal = ('groups', 'user_permissions',)


# admin.site.register(User, UserAdmin)