import imp
from django.contrib import admin
from student.models import Logo, Signature, Designcert, PartLogo, Payment,PDFDocument, DocPayment, CertificatePayment, EbooksPayment
# from student.models import Cart,CartItem, Order, OrderItem

from django.contrib import admin
from django.contrib import admin
from .models import  Question, Choice

from sms.models import  Topics



admin.site.register(PDFDocument)
# admin.site.register(DocPayment)
admin.site.register(CertificatePayment)
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