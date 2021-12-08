from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import Profile
from users.models import NewUser
from django.contrib.auth import get_user_model
User = get_user_model()

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password','Country', 'Phone_number','last_login')}),
        ('Permissions', {'fields': (
            'is_active', 
            'is_staff', 
            'is_superuser',
            'groups', 
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('First_name','Last_name','email','Country','Phone_number' ,'password1', 'password2')
            }
        ),
    )

    list_display = ('First_name','Last_name', 'email','Country', 'Phone_number','is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(NewUser, UserAdmin)
# admin.site.register(Profile)
