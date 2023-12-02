import imp
from django.contrib import admin
from student.models import (Logo, Signature, Designcert, 
                            PartLogo, Payment,PDFDocument, 
                            DocPayment, CertificatePayment, 
                            EbooksPayment, ReferrerMentor
                            )

# from student.models import Cart,CartItem, Order, OrderItem

from import_export.admin import ImportExportModelAdmin
from import_export import fields,resources
from import_export.widgets import ForeignKeyWidget
from django.contrib import admin

from .models import  Question, Choice

from sms.models import  Topics



admin.site.register(PDFDocument)
# admin.site.register(ReferrerMentor)
class ReferrerMentorAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'learner', ' referrer_code', 'referrer', 'referred_students']
    list_filter = ['id', 'user', 'referrer']
    search_fields = ['id', 'name', 'referrer']
    ordering = ['id']

    resource_class = ReferrerMentor

admin.site.register(ReferrerMentor, ReferrerMentorAdmin)


# admin.site.register(CertificatePayment)
class CertificatePaymentResource(resources.ModelResource):
    
    courses = fields.Field(
        column_name= 'courses',
        attribute='courses',
        widget=ForeignKeyWidget(CertificatePayment,'title') )
    
    class Meta:
        model = CertificatePayment
        # fields = ('title',)

class CertificatePaymentAdmin(ImportExportModelAdmin):
    list_display = ['id','amount','ref', 'first_name', 'last_name', 'content_type', 'email', 'verified', 'date_created']
    # prepopulated_fields = {"courses": ("courses",)}
    list_filter = ['amount', 'courses__title','ref', 'email','date_created']
    search_fields = ['id', 'amount', 'courses__title','date_created', 'email']  # Use double underscore for related fields
    ordering = ['amount']
    resource_class = CertificatePaymentResource

    def get_courses_titles(self, obj):
        # Get a comma-separated list of course titles
        return ', '.join(course.title for course in obj.courses.all())

    

admin.site.register(CertificatePayment, CertificatePaymentAdmin)


admin.site.register(EbooksPayment)

admin.site.register(Payment)

# Register your models here.
class LogoAdmin(admin.ModelAdmin):
    list_display = ("logo",)

admin.site.register(Logo,  LogoAdmin)

class PartLogoAdmin(admin.ModelAdmin):
    list_display = ("logo",)

admin.site.register(PartLogo,  LogoAdmin)

class SignatureAdmin(admin.ModelAdmin):
    list_display = ("sign",)

admin.site.register(Signature,  SignatureAdmin)

class DesigncertAdmin(admin.ModelAdmin):
    list_display = ("design",)

admin.site.register(Designcert,  DesigncertAdmin)