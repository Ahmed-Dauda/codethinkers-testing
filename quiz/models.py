from django.db import models
# from student.models import Student
from users.models import Profile, NewUser
from cloudinary.models import CloudinaryField
from sms.models import Courses as smscourses
from tinymce.models import HTMLField
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
    option = models.CharField(max_length=100,blank=True, null= True)
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

class School(models.Model):
    name = models.CharField(max_length=255)
    school_name = models.CharField(max_length=255)
    portfolio = models.CharField(max_length=255, blank=True, null= True)
    logo = CloudinaryField('school_logos', blank=True, null= True)
    principal_signature = CloudinaryField('principal_signatures', blank=True, null= True)
    created = models.DateTimeField(auto_now_add=True,blank=True, null= True)
    updated = models.DateTimeField(auto_now=True, blank=True, null= True)

    def __str__(self):
        return f"{self.school_name}"


    
class Course(models.Model):

#    course_name = models.CharField(max_length=50, unique= True)
   course_name = models.ForeignKey(Courses,on_delete=models.CASCADE, blank=True, null= True)
#    school = models.ForeignKey(School, on_delete=models.SET_NULL, blank=True, null=True)
#    schools = models.ManyToManyField(School , related_name='courses', blank=True)
   partdesc1 = models.CharField(max_length=300, blank=True, null= True)
   img_partdesc1 = CloudinaryField('image', blank=True, null= True)
   partdesc2 = models.CharField(max_length=225, blank=True, null= True)
   img_partdesc2 = CloudinaryField('image', blank=True, null= True)
   partdesc3 = models.CharField(max_length=225, blank=True, null= True)
   signature = CloudinaryField('signature', blank=True, null= True)
   signby = models.CharField(max_length=229, blank=True, null= True)
   signby_portfolio = models.CharField(max_length=229 ,blank=True, null= True)
   question_number = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   pass_mark = models.PositiveIntegerField(null=True)
   duration_minutes = models.PositiveIntegerField(default=10)  # Add this field for quiz duration
   created = models.DateTimeField(auto_now_add=True,blank=True, null= True)
   updated = models.DateTimeField(auto_now=True, blank=True, null= True)
   id = models.AutoField(primary_key=True)

   
   def __str__(self):
        return f'{self.course_name}'

# class Student(models.Model):
#     user = models.OneToOneField(Profile, on_delete=models.CASCADE, blank=True, null=True)
#     school = models.ForeignKey(School, on_delete=models.SET_NULL, blank=True, null=True)
#     name = models.CharField(max_length=255)
#     admission_no = models.CharField(max_length=20, unique=True)
#     date_of_birth = models.DateField()
#     address = models.CharField(max_length=255)
#     # course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True)

#     def __str__(self):
#         school_name = getattr(self.school, 'school_name', '')
#         return f'{self.name} - {self.school.school_name} {self.id}'


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


