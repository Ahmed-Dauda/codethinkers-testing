import imp
from django.contrib import admin
from student.models import Logo, signature, Designcert, PartLogo, Certificate


admin.site.register(Certificate)
# Register your models here.
class LogoAdmin(admin.ModelAdmin):
    list_display = ("logo",)

admin.site.register(Logo,  LogoAdmin)

class PartLogoAdmin(admin.ModelAdmin):
    list_display = ("logo",)

admin.site.register(PartLogo,  LogoAdmin)

class SignatureAdmin(admin.ModelAdmin):
    list_display = ("sign",)

admin.site.register(signature,  SignatureAdmin)

class DesigncertAdmin(admin.ModelAdmin):
    list_display = ("design",)

admin.site.register(Designcert,  DesigncertAdmin)