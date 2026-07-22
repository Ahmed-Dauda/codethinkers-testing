from django.contrib import admin
from .models import Student, Teacher, Course, Attendance, DailyShopRecord, LightViolation

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'grade', 'created_at')
    search_fields = ('name',)
    list_filter = ('grade',)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'created_at')
    search_fields = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'created_at')
    search_fields = ('title',)
    list_filter = ('teacher',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'status')
    search_fields = ('student__name', 'course__title')

@admin.register(DailyShopRecord)
class DailyShopRecordAdmin(admin.ModelAdmin):
    list_display = ('date', 'item_name', 'amount_spent')
    search_fields = ('item_name',)
    list_filter = ('date',)

@admin.register(LightViolation)
class LightViolationAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'description')
    search_fields = ('student__name', 'description')
    list_filter = ('date',)