from typing import cast
from django.contrib.contenttypes.fields import GenericRelation
from django.forms import Widget
from users.models import Profile
from django.db import models
from django.db.models.deletion import CASCADE
from users.models import NewUser
from cloudinary.models import CloudinaryField
from django.db import models
from embed_video.fields import EmbedVideoField
from django.conf import settings
from hitcount.models import HitCount, HitCountMixin
from django.db import models
from tinymce.models import HTMLField
from tinymce import models as tinymce_models
from tinymce.widgets import TinyMCE
# Create your models here.


class Categories(models.Model, HitCountMixin):
   
    
    name = models.CharField(max_length=225, blank=True, null= True, unique=True)
    desc = models.TextField( blank=True, null= True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null= True)
    updated = models.DateTimeField(auto_now=True, blank=True, null= True)
    img_cat = CloudinaryField('image', blank=True, null= True)
    # object_pk = models.PositiveIntegerField(default=True)
    hit_count_generic = GenericRelation(
    HitCount, object_id_field='object_pk',
    related_query_name='hit_count_generic_relation')

# 
    def __str__(self):
        return f'{self.name}'

 

class Courses(models.Model):
    
    COURSE_TYPE = [
    ('Course','COURSE'),
    ('Professional Certificate', 'PROFESSIONAL CERTIFICATE'),
    ('Specialization', 'SPECIALIZATION'),
    ('Degree', 'DEGREE'),
     ('Diploma', 'DIPLOMA'),
    ]

    PAYMENT_CHOICES = [
    ('Premium','PREMIUM'),
    ('Free', 'FREE'),
    ('Sponsored', 'SPONSORED'),
  
    ]
    img_course = CloudinaryField('image', blank=True, null= True)
    categories =models.ForeignKey(Categories, on_delete= models.CASCADE, related_name='categories')
    title = models.CharField(max_length=225, blank=True, null= True)
    course_logo = CloudinaryField('course_logo', blank=True, null= True)
    course_owner = models.CharField(max_length=225, blank=True, null= True)
    course_type = models.CharField(choices = COURSE_TYPE, default='course' , max_length=225, blank=True, null= True)
    status_type = models.CharField (choices = PAYMENT_CHOICES, default='premium' ,max_length=225, blank=True, null= True)
    price = models.DecimalField (max_digits=10, decimal_places=2, default= '20000' ,max_length=225, blank=True, null= True)
    desc = tinymce_models.HTMLField(blank=True, null= True)

    # partdesc1 = models.CharField(max_length=300, blank=True, null= True)
    # img_partdesc1 = CloudinaryField('image', blank=True, null= True)
    # partdesc2 = models.CharField(max_length=229, blank=True, null= True)
    # img_partdesc2 = CloudinaryField('image', blank=True, null= True)
    # partdesc3 = models.CharField(max_length=225, blank=True, null= True)
    desc_home = tinymce_models.HTMLField( blank=True, null= True)
    course_desc = tinymce_models.HTMLField(blank=True, null= True)
    course_link = models.URLField(max_length=225, blank=True, null= True)
    created = models.DateTimeField(auto_now_add=True,blank=True, null= True)
    updated = models.DateTimeField(auto_now=True, blank=True, null= True)
    hit_count_generic = GenericRelation(
    HitCount, object_id_field='object_pk',
    related_query_name='hit_count_generic_relation')

    def __str__(self):
        return f'{self.title}'


class Topics(models.Model):
    
    categories=models.ForeignKey(Categories, on_delete= models.CASCADE)
    courses=models.ForeignKey(Courses, on_delete= models.CASCADE) 
    title = models.CharField(max_length=500, blank=True, null= True)
    slug = models.SlugField(max_length=500)
    # objectives = tinymce_models.HTMLField(null= True,blank=True,)
    desc = tinymce_models.HTMLField( blank=True, null= True)
    # desc_home = tinymce_models.HTMLField( blank=True, null= True)
    coursedesc = tinymce_models.HTMLField( blank=True, null= True)
    # student_activity = tinymce_models.HTMLField(null= True,blank=True,)
    # evaluation = models.TextField(blank=True, null= True)
    img_topic = CloudinaryField('image', blank=True, null= True)
    img_tutorial = CloudinaryField('image', blank=True, null= True)
    video = EmbedVideoField(blank=True, null= True)  # same like models.URLField()
    topics_url = models.CharField(max_length=500, blank=True, null= True)
    created = models.DateTimeField(auto_now_add=True,blank=True, null= True)
    updated = models.DateTimeField(auto_now=True, blank=True, null= True)
    id = models.BigAutoField(primary_key=True)
    hit_count_generic = GenericRelation(
    HitCount, object_id_field='object_pk',
    related_query_name='hit_count_generic_relation')


    def __str__(self):
        return f'{self.title}-----{self.courses}'


# class PhotoGallery(models.Model):
   
#     name = models.CharField(max_length=225, blank=True, null= True, unique=True)
#     created = models.DateTimeField(auto_now_add=True, blank=True, null= True)
#     updated = models.DateTimeField(auto_now=True, blank=True, null= True)
#     img_cat = CloudinaryField('image', blank=True, null= True)
#     # object_pk = models.PositiveIntegerField(default=True)

#     def __str__(self):
#         return f'{self.name}'


class Comment(models.Model):
    
    username = models.CharField(default='fff', max_length=225, blank=True, null= True, unique=True)
    first_name = models.CharField(default='fff', max_length=225, blank=True, null= True)
    last_name = models.CharField(max_length=225, blank=True, null= True)
    title = models.CharField(max_length=225,  null=True, blank =True )
    desc = tinymce_models.HTMLField(max_length=500, blank=True, null= True)
    created = models.DateTimeField(auto_now_add=True,blank=True, null= True)
    updated = models.DateTimeField(auto_now=True, blank=True, null= True)
    # id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return f'{self.title}'

class Blog(models.Model):

    author=models.ForeignKey(Profile,on_delete=models.CASCADE, blank=True, null= True)
    poster = models.CharField(max_length=225,  null=True, blank =True )
    title = models.CharField(max_length=225,  null=True, blank =True )
    img_source = models.CharField(max_length=225, null= True)
    slug = models.SlugField(null=False, unique=True) 
    img_blog = CloudinaryField('image', blank=True, null= True)
    desc = tinymce_models.HTMLField( blank=True, null= True)
    created = models.DateTimeField(auto_now_add=True,blank=True, null= True)
    updated = models.DateTimeField(auto_now=True, blank=True, null= True)
    hit_count_generic = GenericRelation(
    HitCount, object_id_field='object_pk',
    related_query_name='hit_count_generic_relation')
    def __str__(self):
        return f'{self.title}'

from django.utils import timezone
from django.urls import reverse
# MainApp/models.py
class Blogcomment(models.Model):
    post = models.ForeignKey(Blog,related_name='comments' ,on_delete=models.SET_NULL, null=True)
    # author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    # subtitle = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True,blank=True, null= True)
    updated = models.DateTimeField(auto_now=True, blank=True, null= True)
   
    img_blogcomment = CloudinaryField('image', blank=True, null= True)
    
    def __str__(self):
        return f'{self.post}'

class Alert(models.Model):

    title = models.CharField(max_length=100, null=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True,blank=True, null= True)
 
    def __str__(self):
        return f'{self.title}'
    
class Gallery(models.Model):

    title = models.CharField(max_length=100, null=True)
    gallery = CloudinaryField('image', blank=True, null= True)
 
    def __str__(self):
        return f'{self.title}'