from typing import cast
from django.contrib.contenttypes.fields import GenericRelation

from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db import models
from embed_video.fields import EmbedVideoField

from hitcount.models import HitCount, HitCountMixin

# Create your models here.


class Categories(models.Model, HitCountMixin):
   
    name = models.CharField(max_length=225, blank=True, null= True, unique=True)
    desc = models.TextField( blank=True, null= True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null= True)
    updated = models.DateTimeField(auto_now=True, blank=True, null= True)
    # object_pk = models.PositiveIntegerField(default=True)
    hit_count_generic = GenericRelation(
    HitCount, object_id_field='object_pk',
    related_query_name='hit_count_generic_relation')

# 
    def __str__(self):
        return f'{self.name}'

class Courses(models.Model):
    
    categories=models.ForeignKey(Categories, on_delete= models.CASCADE)
    title = models.CharField(max_length=225, default='')
    desc = models.TextField(default='')
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
    title = models.CharField(max_length=225, blank=True, null= True, unique=True)
    objectives = models.TextField( blank=True, null= True)
    desc = models.TextField( blank=True, null= True)
    student_activity = models.TextField(blank=True, null= True)
    evaluation = models.TextField(blank=True, null= True)
    img_topic = CloudinaryField('image', blank=True, null= True)
    img_tutorial = CloudinaryField('image', blank=True, null= True)
    video = EmbedVideoField(blank=True, null= True)  # same like models.URLField()
    # img_topic = models.ImageField(blank = True, null = True)
    top_urls = [
        ('https://t.me/joinchat/4F9VVjDPLzAwM2Q0', 'Beginners python_url'),
        ('https://t.me/joinchat/5CBRm0mlq5VlZmE0', 'Beginners html_url'),
        ('https://t.me/joinchat/8qkzp31B9EE1YjY0', 'Beginners statistic_url'),
        ('https://t.me/joinchat/xRjZ9vXkUx43NmY0', 'Beginners django_url'),
        ('https://t.me/joinchat/hgBXeiRmfDA1M2M0', 'Beginners sql_url'),
        ('https://t.me/joinchat/NF7h8BKK_vFjOTk8', 'Beginners javascripts_url'),
        
    ]
    topics_url = models.CharField(max_length=500, choices= top_urls, blank=True, null= True)
    created = models.DateTimeField(auto_now_add=True,blank=True, null= True)
    updated = models.DateTimeField(auto_now=True, blank=True, null= True)
    # pk = models.BigAutoField(primary_key=True)
    hit_count_generic = GenericRelation(
    HitCount, object_id_field='object_pk',
    related_query_name='hit_count_generic_relation')

    def __str__(self):
        return f'{self.title}'

class Comment(models.Model):
    
    username = models.CharField(default='fff', max_length=225, blank=True, null= True, unique=True)
    first_name = models.CharField(default='fff', max_length=225, blank=True, null= True)
    last_name = models.CharField(max_length=225, blank=True, null= True)
    title = models.CharField(max_length=225,  null=True, blank =True )
    desc = models.TextField(max_length=500, blank=True, null= True)
    created = models.DateTimeField(auto_now_add=True,blank=True, null= True)
    updated = models.DateTimeField(auto_now=True, blank=True, null= True)
    # id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return f'{self.title}'

class Blog(models.Model):
    title = models.CharField(max_length=225, blank=True, null= True, unique=True)
    img_blog = CloudinaryField('image', blank=True, null= True)
    desc = models.TextField( blank=True, null= True)
    created = models.DateTimeField(auto_now_add=True,blank=True, null= True)
    updated = models.DateTimeField(auto_now=True, blank=True, null= True)
    hit_count_generic = GenericRelation(
    HitCount, object_id_field='object_pk',
    related_query_name='hit_count_generic_relation')
    def __str__(self):
        return f'{self.title}'