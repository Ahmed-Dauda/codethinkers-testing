from django.db import models
from cloudinary.models import CloudinaryField
# from users.models import NewUser
# from django.conf import settings


class Logo(models.Model):
   
   logo = CloudinaryField('image', blank=True, null= True)
   
   def __str__(self):
        return f"{self.logo}"

class signature(models.Model):
       
   sign = CloudinaryField('image', blank=True, null= True)
   
   def __str__(self):
        return f"{self.sign}"  


    # @property
    # def get_name(self):
    #     return self.user.first_name+" "+self.user.last_name
    # @property
    # def get_instance(self):
    #     return self
    # def __str__(self):
    #     return self.user.first_name
