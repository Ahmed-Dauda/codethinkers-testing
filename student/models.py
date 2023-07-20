from django.db import models
from cloudinary.models import CloudinaryField
# from users.models import NewUser
# from django.conf import settings
from cloudinary.models import CloudinaryField
from tinymce.models import HTMLField
from tinymce import models as tinymce_models
import secrets
from django.conf import settings
import uuid
import random
import string
from django.contrib import messages



# from sms.paystack import Paystack

from django.db import models
from django.contrib.auth.models import User

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
   
class signature(models.Model):
       
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

# class UserWallet(models.Model):
#     user = models.OneToOneField(Profile, null=True, on_delete=models.CASCADE)
#     currency = models.CharField(max_length=50, default='NGN', null=True)
#     created_at = models.DateTimeField(default=timezone.now, null=True)

#     def _str_(self):
#         return self.user._str_()
from sms.models import Courses


class Payment(models.Model):
    user = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    courses = models.ForeignKey(Courses, null=True, on_delete=models.CASCADE, related_name='payments')
    amount = models.PositiveBigIntegerField(null=True)
    ref = models.CharField(max_length=250, null=True)
    first_name = models.CharField(max_length=250, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):

        return f"Payment: {self.amount}"


class Cart(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Courses, through='CartItem')
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
            ordering = ('-created',)

    def __str__(self):

        return f"{self.user} "

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
            ordering = ('-created',)

    def __str__(self):

        return f"{self.cart} {self.quantity}"

class Order(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Courses, through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_reference = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
            ordering = ('-created',)

    def __str__(self):

        return f"{self.user}  {self.total_amount}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
            ordering = ('-created',)

    def __str__(self):

        return f"{self.order}  {self.quantity}"

        
# end of payment logics 


    

    # def save(self, *args, **kwargs):
    #     if not self.ref:
    #         while True:
    #             ref = secrets.token_urlsafe(50)
    #             object_with_similar_ref = Payment.objects.filter(ref=ref)
    #             if not object_with_similar_ref:
    #                 self.ref = ref
                   

    #     super().save(*args, **kwargs)

    # def amount_value(self) -> int:
    #     return self.amount * 100

    # def verify_payment(self):
    #     payment = Paystack()
    #     status, result = payment.verify_payment(self.ref, self.amount)
    #     if status:
    #         if result["amount"] / 100 == self.amount():
    #             self.verified = True
    #         self.save()

    #     if self.verified:
    #         return True

    #     return False
        