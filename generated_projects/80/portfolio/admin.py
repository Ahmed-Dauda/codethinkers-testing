from django.contrib import admin
from .models import Skill, Project, Experience, About, Comment

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'created_at')
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'image', 'created_at')
    search_fields = ('title',)

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company', 'start_date', 'end_date', 'image')
    search_fields = ('job_title', 'company')

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('title', 'comment', 'created_at')  # Updated to include comment
    search_fields = ('title', 'comment')  # Updated to include comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'project', 'experience', 'created_at')
    search_fields = ('content',)