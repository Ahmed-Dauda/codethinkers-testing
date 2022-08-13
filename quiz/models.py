from django.db import models
# from student.models import Student
from users.models import Profile
from cloudinary.models import CloudinaryField

class Course(models.Model):
   course_name = models.CharField(max_length=50, unique= True)
   question_number = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   pass_mark = models.PositiveIntegerField(null=True)
   constant = models.PositiveIntegerField(null=True, default=2)
   created = models.DateTimeField(auto_now_add=True,blank=True, null= True)
   updated = models.DateTimeField(auto_now=True, blank=True, null= True)
   id = models.AutoField(primary_key=True)
   
   def __str__(self):
        return f'{self.course_name}'

class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=models.TextField(blank=True, null = True)
    img_quiz = CloudinaryField('image', blank=True, null= True)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
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
    constant = models.PositiveIntegerField(null=True, default=2)
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

