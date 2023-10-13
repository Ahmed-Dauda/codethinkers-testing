from django.db import models
# from student.models import Student
from users.models import Profile
from cloudinary.models import CloudinaryField
from sms.models import Courses as smscourses

from sms.models import Courses, Topics


# assessment models 

class TopicsAssessment(models.Model):
#    course_name = models.CharField(max_length=50, unique= True)
   course_name = models.ForeignKey(Topics,on_delete=models.CASCADE, blank=True, null= True)
   question_number = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   pass_mark = models.PositiveIntegerField(null=True)

   created = models.DateTimeField(auto_now_add=True,blank=True, null= True)
   updated = models.DateTimeField(auto_now=True, blank=True, null= True)
   id = models.AutoField(primary_key=True)
   
   def __str__(self):
        return f'{self.course_name}'


from tinymce.models import HTMLField


class QuestionAssessment(models.Model):
    course=models.ForeignKey(TopicsAssessment,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    # question= models.TextField( blank=True, null= True)
    question= HTMLField( blank=True, null= True)
    img_quiz = CloudinaryField('image', blank=True, null= True)
    option1 = HTMLField(max_length=500, null= True)
    option2 = HTMLField(max_length=500, null= True)
    option3 = HTMLField(max_length=500, null= True)
    option4 = HTMLField(max_length=500, null= True)

    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)
    created = models.DateTimeField(auto_now_add=True,blank=True, null= True)
    updated = models.DateTimeField(auto_now=True, blank=True, null= True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.course} | {self.question}"
    
class ResultAssessment(models.Model):

    student = models.ForeignKey(Profile,on_delete=models.CASCADE)
    exam = models.ForeignKey(TopicsAssessment,on_delete=models.CASCADE)
    # smscourses = models.ForeignKey(smscourses,on_delete=models.CASCADE, blank=True, null= True)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
    # pass_mark = models.PositiveIntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True,blank=True, null= True)
    updated = models.DateTimeField(auto_now=True, blank=True, null= True)
    id = models.AutoField(primary_key=True)
    def __str__(self):
        return f"{self.student}---{self.exam.course_name}----{self.marks}"

# end


class Course(models.Model):
#    course_name = models.CharField(max_length=50, unique= True)
   course_name = models.ForeignKey(Courses,on_delete=models.CASCADE, blank=True, null= True)
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
#    cert_price = models.DecimalField(max_digits=10, decimal_places=0, default='1000', max_length=225, blank=True, null=True)
   created = models.DateTimeField(auto_now_add=True,blank=True, null= True)
   updated = models.DateTimeField(auto_now=True, blank=True, null= True)
   id = models.AutoField(primary_key=True)
   
   def __str__(self):
        return f'{self.course_name.title}'

from tinymce.models import HTMLField


class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    # question= models.TextField( blank=True, null= True)
    question= HTMLField( blank=True, null= True)
    img_quiz = CloudinaryField('image', blank=True, null= True)
    option1 = HTMLField(max_length=500, null= True)
    option2 = HTMLField(max_length=500, null= True)
    option3 = HTMLField(max_length=500, null= True)
    option4 = HTMLField(max_length=500, null= True)

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
    # smscourses = models.ForeignKey(smscourses,on_delete=models.CASCADE, blank=True, null= True)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
    # pass_mark = models.PositiveIntegerField(null=True)
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

