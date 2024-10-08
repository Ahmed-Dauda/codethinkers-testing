import imp
from django.contrib import admin
from student.models import (Logo, Signature, Designcert,Certificate, 
                            PartLogo, Payment,PDFDocument, 
                            DocPayment, CertificatePayment, 
                            EbooksPayment, ReferrerMentor, PercentageReferrer
                            )

# from student.models import Cart,CartItem, Order, OrderItem
from django.db.models import Sum
from import_export.admin import ImportExportModelAdmin
from import_export import fields,resources
from import_export.widgets import ForeignKeyWidget
from django.contrib import admin
from users.models import NewUser
from .models import  Question, Choice
from django.db.models import Q 
from sms.models import  Topics
from django.utils.html import format_html
from .models import AdvertisementImage

# admin.site.register(Certificate)
admin.site.register(PDFDocument)
admin.site.register(PercentageReferrer)

class CertificateAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','course', 'code')

admin.site.register(Certificate, CertificateAdmin)


class AdvertisementImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'desc')

admin.site.register(AdvertisementImage, AdvertisementImageAdmin)

class ReferrerMentorResource(resources.ModelResource):
    user = fields.Field(
        # column_name='referrer',
        # attribute='referrer',
        widget=ForeignKeyWidget(NewUser, 'referrer')
    )

    class Meta:
        model = ReferrerMentor

class ReferrerMentorAdmin(ImportExportModelAdmin):
    list_display = [
        'name', 'referrer', 'get_f_code_count','get_total_amount',
        'referrer_code', 'account_number', 'bank', 'phone_no', 'date_created'
    ]
    list_filter = ['name', 'referrer', 'referrer_code']
    search_fields = ['name', 'referrer', 'referrer_code']
    ordering = ['id']

    resource_class = ReferrerMentorResource

    def get_referred_students_count(self, obj):
        return obj.referred_students.count()

    get_referred_students_count.short_description = 'Referred Students Count'

    def get_f_code_count(self, obj):
        get_f_code_count = CertificatePayment.objects.filter(f_code=obj.referrer_code).count()
        get_f_code_count +=Payment.objects.filter(f_code=obj.referrer_code).count()
        return get_f_code_count

    get_f_code_count.short_description = 'Count earnings'

    # def Count_of_students_referred(self, obj):
  
    #     # Use a list comprehension to get phone numbers, join by commas
    #     phone_numbers = NewUser.objects.filter(phone_number=obj.referrer_code)
    #     # print('phone nu', phone_numbers)
    #     return len(phone_numbers)

    # Count_of_students_referred.short_description = 'Count of students referred'

    def get_total_amount(self, obj):
        cert_payment_sum = CertificatePayment.objects.filter(f_code=obj.referrer_code).aggregate(Sum('amount'))['amount__sum'] or 0
        payment_sum = Payment.objects.filter(f_code=obj.referrer_code).aggregate(Sum('amount'))['amount__sum'] or 0
        
        total_amount = cert_payment_sum + payment_sum
        
        if total_amount:
            referer_per = PercentageReferrer.objects.all().first().referer_per
            # referer_per = int(referer_per)
            total_amount *= int(referer_per)/100
        return total_amount or 0

    # def get_total_amount(self, obj):
    #     total_amount = CertificatePayment.objects.filter(f_code=obj.referrer_code).aggregate(Sum('amount'))['amount__sum']
    #     total_amount += Payment.objects.filter(f_code=obj.referrer_code).aggregate(Sum('amount'))['amount__sum']
    #     if total_amount is not None:
    #         total_amount *= 0.2
    #         return total_amount 
    #     else:
    #         return 0  # 
        
        # if total_amount is not None:
        #     return total_amount *= 0.2
        # else:
        #     return 0  # 

    get_total_amount.short_description = 'Total Amount (#)'

    def related_payments(self, obj):
        payments = CertificatePayment.objects.filter(f_code=obj.referrer_code)
        return ", ".join([f"{payment.amount} ({', '.join(payment.courses.values_list('title', flat=True))})" for payment in payments])

    related_payments.short_description = 'Related Payments'


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
    list_display = ['email', 'amount', 'ref', 'f_code','first_name','last_name','get_courses_titles' ,'content_type', 'verified', 'date_created']
    list_filter = ['amount', 'f_code', 'content_type', 'ref', 'email', 'date_created']
    search_fields = ['amount','email','f_code', 'content_type','date_created']
    ordering = ['amount']
    resource_class = CertificatePaymentResource

    def get_courses_titles(self, obj):
        # Get a comma-separated list of course titles for the CertificatePayment instance (obj)

        return ', '.join(course.course_name.title for course in obj.courses.all())

    get_courses_titles.short_description = 'Courses'  # Set a user-friendly name for the column


    get_courses_titles.short_description = 'Courses'  # Set a user-friendly name for the column

admin.site.register(CertificatePayment, CertificatePaymentAdmin)




admin.site.register(EbooksPayment)

# admin.site.register(Payment)
from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('email' ,'get_course_titles','content_type','first_name','first_name','amount','ref','f_code' , 'verified', 'date_created')
    list_filter = ('content_type','email','verified','ref','f_code', 'date_created')
    search_fields = ('ref','f_code', 'email','content_type', 'amount', 'courses__title')
    # search_fields = ('payment_user__user__username','ref','f_code', 'email','content_type', 'amount', 'courses__title')

    def get_course_titles(self, obj):
        return ', '.join(course.title for course in obj.courses.all())

    get_course_titles.short_description = 'Courses'


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