from django.db import models
from users.models import NewUser
from django.conf import settings


class Student(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Student/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.user}"
   


    # @property
    # def get_name(self):
    #     return self.user.first_name+" "+self.user.last_name
    # @property
    # def get_instance(self):
    #     return self
    # def __str__(self):
    #     return self.user.first_name
