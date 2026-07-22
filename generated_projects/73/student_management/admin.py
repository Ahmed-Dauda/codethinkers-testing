from django.contrib import admin
from .models import Student, Class, Teacher

admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Teacher)