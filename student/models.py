from django.db import models
from cloudinary.models import CloudinaryField

from users.models import NewUser
from quiz import models as QMODEL
import secrets
from django.conf import settings
import uuid
import random
import string
from django.contrib import messages



# from sms.paystack import Paystack


from django.contrib.auth.models import User

from django.db import models
from sms.models import Topics



class Question(models.Model):
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


def generate_certificate_code():
    code_length = 10
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(code_length))


class Certificate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null= True)
    code = models.CharField(max_length=10, unique=True, default=generate_certificate_code)
    holder = models.CharField(max_length=255, null= True)
    issued_date = models.DateField(null= True)

    # Add any additional fields relevant to the certificate

    def __str__(self):
        return self.holder



class Logo(models.Model):
   
   logo = CloudinaryField('image', blank=True, null= True)
   
   def __str__(self):
        return f"{self.logo}"

class PartLogo(models.Model):
   
   logo = CloudinaryField('image', blank=True, null= True)
   
   def __str__(self):
        return f"{self.logo}"
   
class Signature(models.Model):
       
   sign = CloudinaryField('image', blank=True, null= True)
   
   def __str__(self):
        return f"{self.sign}"  

class Designcert(models.Model):
       
   design = CloudinaryField('image', blank=True, null= True)
   
   def __str__(self):
        return f"{self.design}"  

from django.db import models
from users.models import Profile 

import secrets
from django.db import models
from sms.paystack import Paystack  # Assuming the Paystack class is imported correctly
from django.utils import timezone



from sms.models import Courses



from django.db import models
from cloudinary.models import CloudinaryField



class PDFDocument(models.Model):
    title = models.CharField(max_length=200)
    desc = models.TextField()
    img_ebook = CloudinaryField('Ebook images', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, default='500', max_length=225, blank=True, null=True)
    # pdf_file = models.FileField(upload_to='pdf_documents/')  
    pdf_url = models.URLField(blank=True, null=True)  # Add the URL field for Google Drive PDF link
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  f"{self.title}"



class EbooksPayment(models.Model):
    payment_user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    courses = models.ManyToManyField(PDFDocument, related_name='ebooks')
    amount = models.PositiveBigIntegerField(null=True)
    ref = models.CharField(max_length=250, null=True)
    first_name = models.CharField(max_length=250, null=True)
    last_name = models.CharField(max_length=200, null=True)
    content_type = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        # Get a comma-separated list of course titles
        # course_titles = ', '.join(course.title for course in self.courses.all())
        return f"{self.payment_user} - {self.content_type} Payment - Amount: {self.amount}"

from quiz.models import Result, Course

class CertificatePayment(models.Model):
    payment_user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    courses = models.ManyToManyField(Course,related_name='certificates',blank=True)
    amount = models.PositiveBigIntegerField(null=True)
    # user_association = models.ForeignKey(NewUser, on_delete=models.CASCADE, null=True)
    # referral_code = models.CharField(max_length=250, null=True, blank=True)
    ref = models.CharField(max_length=250, null=True)
    f_code = models.CharField(max_length=200, null=True, blank=True)
    first_name = models.CharField(max_length=250, null=True)
    last_name = models.CharField(max_length=200, null=True)
    content_type = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    # def __str__(self):
    #     return self.content_type

    def __str__(self):
    # Get a comma-separated list of course titles
        course_t = ', '.join(course.course_name for course in self.courses.all())
        return f"{self.payment_user} - {self.content_type} Payment - Amount: {self.amount} - Courses: {course_t}"


    # def __str__(self):
    #     # Get a comma-separated list of course titles
    #     course_titles = ', '.join(course.title for course in self.courses.all())
    #     # Get the associated Profile
    #     payment_user_profile = self.payment_user

    #     # Initialize referrer_code as None
    #     referrer_code = None

    #     # Check if the user has a profile
    #     if payment_user_profile:
    #         # Check if the profile has a referrer_profile
    #         referrer_profile = payment_user_profile.referrer_profile
    #         if referrer_profile:
    #             # Get the referrer code
    #             referrer_code = referrer_profile.referral_code

    #     return f"{self.payment_user} - {self.content_type} Payment - Amount: {self.amount} - Courses: {course_titles} - Referrer Code: {referrer_code}"
     


class DocPayment(models.Model):
    payment_user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    pdfdocument = models.ManyToManyField(PDFDocument, related_name='docpayments')
    amount = models.PositiveBigIntegerField(null=True)
    ref = models.CharField(max_length=250, null=True)
    first_name = models.CharField(max_length=250, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):

        # Get a comma-separated list of course titles
        course_titles = ', '.join(course.title for course in self.pdfdocument.all())
        return f"{self.payment_user} {self.amount} {course_titles}"



class Payment(models.Model):
    payment_user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    courses = models.ManyToManyField(Courses, related_name='payments', blank=True)
    amount = models.PositiveBigIntegerField(null=True)
    ref = models.CharField(max_length=250, null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    content_type = models.CharField(max_length=200, null=True)
    # referral_code = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        # Get a comma-separated list of course titles
        course_titles = ', '.join(course.title for course in self.courses.all())
        return f"{self.payment_user} - {self.content_type} Payment - Amount: {self.amount} - Courses: {course_titles}"


from django.db import models
from django.contrib import admin
from django.db.models import Count, Q
from django.db import models
from django.db.models import Count, Sum

class ReferrerMentor(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    courses = models.ManyToManyField(Courses, related_name='referrercourses', blank=True)
    referrer_code = models.CharField(max_length=20, blank=True, null=True)
    referrer = models.ForeignKey(NewUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='referred_users')
    referred_students = models.ManyToManyField(NewUser, related_name='referrer_profiles', blank=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    bank = models.CharField(max_length=50, blank=True, null=True)
    phone_no = models.CharField(max_length=50, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    @property
    def count_of_students_referred(self):
        phone_numbers = NewUser.objects.filter(phone_number=self.referrer_code)
        return phone_numbers.count()
    
    @property
    def referred_students_count(self):
        return self.referred_students.count()
    
    @property
    def referred_students_phone_numbers(self):
        return self.referred_students.values_list('phone_number', flat=True)
    

    @property
    def f_code_count(self):
        return CertificatePayment.objects.filter(f_code=self.referrer_code).count()

    @property
    def total_amount(self):
        return CertificatePayment.objects.filter(f_code=self.referrer_code).aggregate(Sum('amount'))['amount__sum']

    @property
    def related_payments(self):
        return CertificatePayment.objects.filter(f_code=self.referrer_code)
    
  

    def __str__(self):
        return f'Referrer Profile for {self.name}'

# class ReferrerMentor(models.Model):
#     name = models.CharField(max_length=20, blank=True, null=True)
#     courses = models.ManyToManyField(Courses, related_name='referrercourses', blank=True)
#     referrer_code = models.CharField(max_length=20, blank=True, null=True)
#     referred_count = models.ForeignKey(CertificatePayment, on_delete=models.SET_NULL, null=True, blank=True, related_name='referred_count')
#     referrer = models.ForeignKey(NewUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='referred_users')
#     referred_students = models.ManyToManyField(NewUser, related_name='referrer_profiles', blank=True)

#     def get_referred_students_count(self):
#         return self.referred_students.count()

#     def __str__(self):
#         return f'Referrer Profile for {self.name}'



# class ReferrerMentor(models.Model):
#     name = models.CharField(max_length=20, blank=True, null=True)
#     # learner = models.OneToOneField(NewUser, on_delete=models.CASCADE, blank=True, null=True)
#     courses = models.ManyToManyField(Courses ,related_name='referrercourses',blank=True)
#     referrer_code = models.CharField(max_length=20, blank=True, null=True)
#     referrer = models.ForeignKey(NewUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='referred_users')
#     referred_students = models.ManyToManyField(NewUser, related_name='referrer_profiles', blank=True)

#     def __str__(self):
#         return f'Referrer Profile for {self.name}'