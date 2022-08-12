from django.contrib import admin
from quiz.models import Certificate_note
# Register your models here.

@admin.register(Certificate_note)
class Certificateadmin(admin.ModelAdmin):
    list_display = ['id','note']
    # prepopulated_fields = {"slug": ("title",)}
    list_filter =  ['note']
    search_fields= ['note']
    ordering = ['created']
    
