from django.db import models
from cloudinary.models import CloudinaryField
# from users.models import NewUser
# from django.conf import settings
from cloudinary.models import CloudinaryField
from tinymce.models import HTMLField
from tinymce import models as tinymce_models

from django.conf import settings
import uuid
import random
import string

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

