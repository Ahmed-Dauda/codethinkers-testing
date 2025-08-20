from django.db import models
# from student.models import Student
from users.models import Profile, NewUser
from cloudinary.models import CloudinaryField
from sms.models import Categories, Courses as smscourses
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
   
   class Meta:
       ordering = ['course_name__title'] 


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


class ExamType(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class Session(models.Model):
    name = models.CharField(max_length=20, unique=True)  # E.g., '2022-2023', '2023-2024'
    
    def __str__(self):
        return self.name

class Term(models.Model):
    name = models.CharField(max_length=20, unique=True)
    order = models.PositiveIntegerField(default=1)  # e.g., 1 for "FIRST," 2 for "SECOND," 3 for "THIRD"

    class Meta:
        ordering = ['order']  # Orders by the custom order field

    def __str__(self):
        return self.name


class Course(models.Model):

    categories = models.ForeignKey(Categories, blank=False, default=1, on_delete=models.SET_NULL, related_name='category', null=True)
    room_name = models.CharField(max_length=100, blank=True, null=True)
    schools = models.ForeignKey("quiz.School", on_delete=models.SET_NULL, related_name='course', blank=True, null=True, db_index=True)
    course_name = models.ForeignKey(Courses, on_delete=models.CASCADE, blank=True, null=True, db_index=True)
    question_number = models.PositiveIntegerField(blank=True, null=True)
    course_pay = models.BooleanField(default=False)
    full_screen = models.BooleanField(default=False)
    total_marks = models.PositiveIntegerField(blank=True, null=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, blank=True, null=True, db_index=True)
    term = models.ForeignKey(Term, on_delete=models.SET_NULL, blank=True, null=True, db_index=True)
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, blank=True, null=True, db_index=True)
    num_attemps = models.PositiveIntegerField(default=4)
    show_questions = models.PositiveIntegerField(default=10)
    pass_mark = models.PositiveIntegerField(null=True)
    duration_minutes = models.PositiveIntegerField(default=10)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        verbose_name = 'Exam'
        verbose_name_plural = 'Exams'
        ordering = ['course_name__title']
        indexes = [
            models.Index(fields=['schools']),
            models.Index(fields=['course_name']),
            models.Index(fields=['session']),
            models.Index(fields=['term']),
            models.Index(fields=['exam_type']),
        ]
 
    def save(self, *args, **kwargs):
        if self.total_marks != self.show_questions:
            self.show_questions = self.total_marks
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.course_name}'

    def get_questions(self):
        return self.question_set.all()[:self.show_questions]


# class Course(models.Model):

#    course_name = models.ForeignKey(Courses,on_delete=models.CASCADE, blank=True, null= True)
#    partdesc1 = models.CharField(max_length=300, blank=True, null= True)
#    img_partdesc1 = CloudinaryField('image', blank=True, null= True)
#    partdesc2 = models.CharField(max_length=225, blank=True, null= True)
#    img_partdesc2 = CloudinaryField('image', blank=True, null= True)
#    partdesc3 = models.CharField(max_length=225, blank=True, null= True)
#    signature = CloudinaryField('signature', blank=True, null= True)
#    signby = models.CharField(max_length=229, blank=True, null= True)
#    signby_portfolio = models.CharField(max_length=229 ,blank=True, null= True)
#    question_number = models.PositiveIntegerField()
#    total_marks = models.PositiveIntegerField()
#    pass_mark = models.PositiveIntegerField(null=True)
#    duration_minutes = models.PositiveIntegerField(default=10)  # Add this field for quiz duration
#    created = models.DateTimeField(auto_now_add=True,blank=True, null= True)
#    updated = models.DateTimeField(auto_now=True, blank=True, null= True)
#    id = models.AutoField(primary_key=True)

#    class Meta:
#         ordering = ['course_name__title']  # Change 'title' to actual field name in Courses model
        
#    def __str__(self):
#         return f'{self.course_name}'


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
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, db_index=True)
    exam = models.ForeignKey(Course, on_delete=models.CASCADE, db_index=True)
    schools = models.ForeignKey(School, on_delete=models.SET_NULL, related_name='courseschool', blank=True, null=True)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)

    result_class = models.CharField(max_length=300, blank=True, null=True, db_index=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, blank=True, null=True, db_index=True)
    term = models.ForeignKey(Term, on_delete=models.SET_NULL, blank=True, null=True, db_index=True)
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, blank=True, null=True, db_index=True)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_locked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'exam', 'session', 'term', 'result_class', 'exam_type')
        ordering = ['student__first_name','student__last_name', 'exam__course_name']  
  
    def __str__(self):
        return f"{self.student}---{self.exam.course_name}---{self.exam_type}---{self.marks}"



class Certificate_note(models.Model):
    
    note = models.TextField(blank=True, null= True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null= True)
    id = models.AutoField(primary_key=True)
    
    def __str__(self):
        return f"{self.note}"

class StudentExamSession(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_order = models.JSONField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course}"


