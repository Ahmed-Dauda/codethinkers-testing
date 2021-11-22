from typing import cast
from django.contrib.contenttypes.fields import GenericRelation

from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User



from hitcount.models import HitCount, HitCountMixin

# Create your models here.


class Categoriess(models.Model, HitCountMixin):
   
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

class Coursess(models.Model):
    
    categories=models.ForeignKey(Categoriess, on_delete= models.CASCADE)
    title = models.CharField(max_length=225, default='')
    desc = models.TextField(default='')
    created = models.DateTimeField(auto_now_add=True,blank=True, null= True)
    updated = models.DateTimeField(auto_now=True, blank=True, null= True)
    hit_count_generic = GenericRelation(
    HitCount, object_id_field='object_pk',
    related_query_name='hit_count_generic_relation')

    def __str__(self):
        return f'{self.title}'

class Topicss(models.Model):
    
    categories=models.ForeignKey(Categoriess, on_delete= models.CASCADE)
    courses=models.ForeignKey(Coursess, on_delete= models.CASCADE)
    title = models.CharField(max_length=225, blank=True, null= True, unique=True)
    objectives = models.TextField( blank=True, null= True)
    descs = models.TextField( blank=True, null= True)
    student_activity = models.TextField(blank=True, null= True)
    evaluation = models.TextField(blank=True, null= True)
    img_topic = models.ImageField(blank = True, null = True)
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

class Comments(models.Model):
    
    # user_name = models.ForeignKey(User, on_delete= models.CASCADE)
    first_name = models.CharField(max_length=225, blank=True, null= True)
    last_name = models.CharField(max_length=225, blank=True, null= True)
    title = models.CharField(max_length=225,  null=True, blank =True )
    desc = models.TextField(blank=True, null= True)
    created = models.DateTimeField(auto_now_add=True,blank=True, null= True)
    updated = models.DateTimeField(auto_now=True, blank=True, null= True)
    # id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return f'{self.title}'
