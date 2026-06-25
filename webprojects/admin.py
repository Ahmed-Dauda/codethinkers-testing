from django.contrib import admin
from .models import Project, File, Folder, StudentProgress
from django.utils.html import format_html

@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "progress_display", "last_updated")
    list_filter = ("course",)
    search_fields = ("student__username",)
    readonly_fields = ("last_updated",)
    ordering = ("-last_updated",)

    def progress_display(self, obj):
        from sms.models import Topics

        if not obj.course:
            return "No Course"

        # IMPORTANT: your Topics model uses 'courses' (plural)
        total_topics = Topics.objects.filter(courses=obj.course).count()

        if total_topics == 0:
            return "0%"

        completed = obj.completed_topics.count()
        percentage = int((completed / total_topics) * 100)

        # Optional: show colored percentage
        color = "green" if percentage == 100 else "orange"

        return format_html(
            '<strong style="color:{};">{}%</strong>',
            color,
            percentage
        )

    progress_display.short_description = "Progress"

# ---------------- Project Admin ----------------
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "course", "created")
    list_filter = ("course", "created")
    search_fields = ("name", "user__email")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    # Auto-assign project owner if not superuser
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = request.user
        super().save_model(request, obj, form, change)


# ---------------- Folder Admin ----------------
@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "get_project_owner", "parent")
    search_fields = ("name",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(project__user=request.user)

    def get_project_owner(self, obj):
        if obj.project:
            return obj.project.user
        return None
    get_project_owner.short_description = "Project Owner"


# ---------------- File Admin ----------------
@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "created_by", "folder", "created")
    list_filter = ("created",)
    search_fields = ("name",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(project__user=request.user)

    # Auto-assign creator
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
