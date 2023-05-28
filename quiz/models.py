from django.db import models
# from student.models import Student
from users.models import Profile
from cloudinary.models import CloudinaryField

from tinymce.models import HTMLField
from tinymce import models as tinymce_models
from tinymce.widgets import TinyMCE

class Course(models.Model):
   course_name = models.CharField(max_length=50, unique= True)

   partdesc1 = models.CharField(max_length=300, blank=True, null= True)
   img_partdesc1 = CloudinaryField('image', blank=True, null= True)
   partdesc2 = models.CharField(max_length=229, blank=True, null= True)
   img_partdesc2 = CloudinaryField('image', blank=True, null= True)
  
   partdesc3 = models.CharField(max_length=225, blank=True, null= True)
   signature = CloudinaryField('signature', blank=True, null= True)
   signby = models.CharField(max_length=229, blank=True, null= True)
   signby_portfolio = models.CharField(max_length=229 ,blank=True, null= True)
   question_number = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   pass_mark = models.PositiveIntegerField(null=True)
#    constant = models.PositiveIntegerField(null=True, default=2)
   created = models.DateTimeField(auto_now_add=True,blank=True, null= True)
   updated = models.DateTimeField(auto_now=True, blank=True, null= True)
   id = models.AutoField(primary_key=True)
   
   def __str__(self):
        return f'{self.course_name}'

class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question= tinymce_models.HTMLField( blank=True, null= True)
    img_quiz = CloudinaryField('image', blank=True, null= True)
    option1=tinymce_models.HTMLField(max_length=200)
    option2= tinymce_models.HTMLField(max_length=200)
    option3= tinymce_models.HTMLField(max_length=200)
    option4=tinymce_models.HTMLField(max_length=200)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)
    created = models.DateTimeField(auto_now_add=True,blank=True, null= True)
    updated = models.DateTimeField(auto_now=True, blank=True, null= True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.course} | {self.question}"
    
class Result(models.Model):

    student = models.ForeignKey(Profile,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
    # constant = models.PositiveIntegerField(null=True, default=2)
    created = models.DateTimeField(auto_now_add=True,blank=True, null= True)
    updated = models.DateTimeField(auto_now=True, blank=True, null= True)
    id = models.AutoField(primary_key=True)
    def __str__(self):
        return f"{self.student}---{self.exam.course_name}----{self.marks}"

class Certificate_note(models.Model):
    
    note = models.TextField(blank=True, null= True)
    
    created = models.DateTimeField(auto_now_add=True, blank=True, null= True)
    id = models.AutoField(primary_key=True)
    
    def __str__(self):
        return f"{self.note}"

