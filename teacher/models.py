from django.db import models
from users.models import NewUser

class Teacher(models.Model):
    user=models.OneToOneField(NewUser,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Teacher/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    status= models.BooleanField(default=False)
    salary=models.PositiveIntegerField(null=True)
    id = models.AutoField(primary_key=True)
    
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name
