# Generated by Django 4.1 on 2023-12-26 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
        ('student', '0013_certificatepayment__cached_course_titles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificatepayment',
            name='_cached_course_titles',
        ),
        migrations.AlterField(
            model_name='certificatepayment',
            name='courses',
            field=models.ManyToManyField(blank=True, related_name='certificates', to='quiz.course'),
        ),
    ]
