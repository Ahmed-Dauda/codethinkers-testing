from django.db import models
from cloudinary.models import CloudinaryField
# from users.models import NewUser
# from django.conf import settings
from cloudinary.models import CloudinaryField


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



from sms.models import Courses

# begin;
# set transaction read write;

#             CREATE TABLE IF NOT EXISTS student_payment (
#                 id SERIAL PRIMARY KEY,
#                 payment_user VARCHAR(200),
#                 amount BIGINT,
#                 ref VARCHAR(250),
#                 first_name VARCHAR(250),
#                 last_name VARCHAR(200),
#                 email VARCHAR,
#                 verified BOOLEAN DEFAULT FALSE,
#                 date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             );

# COMMIT;

  


class Payment(models.Model):
    # user = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    payment_user = models.CharField(max_length=200, null=True)
    courses = models.ForeignKey(Courses, null=True, on_delete=models.CASCADE,  related_name='payments')
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


