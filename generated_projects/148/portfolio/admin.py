from django.contrib import admin
from .models import Hero, AboutMe, Skill, Project, Experience, ContactFormSubmission, AboutMe, Skill, Project, Experience, ContactFormSubmission

class ExportAdminMixin:
    actions = ['export_as_csv', 'export_as_docx']

    def export_as_csv(self, request, queryset):
        # CSV export logic
        pass

    def export_as_docx(self, request, queryset):
        # DOCX export logic
        pass

    export_as_csv.short_description = 'Export selected as CSV'
    export_as_docx.short_description = 'Export selected as Word document'

@admin.register(Hero)
class HeroAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'subtitle')
    list_filter = ('title',)
    search_fields = ('title', 'subtitle')

@admin.register(AboutMe)
class AboutMeAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ('content',)

@admin.register(Skill)
class SkillAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'proficiency')
    list_filter = ('proficiency',)
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'link')
    search_fields = ('title',)

@admin.register(Experience)
class ExperienceAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ('job_title', 'company')
    search_fields = ('job_title', 'company')

@admin.register(ContactFormSubmission)
class ContactFormSubmissionAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')