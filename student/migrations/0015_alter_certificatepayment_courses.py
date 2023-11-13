# Generated by Django 4.1 on 2023-11-09 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0017_remove_course_cert_price'),
        ('student', '0014_remove_ebookspayment_courses_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificatepayment',
            name='courses',
            field=models.ManyToManyField(related_name='certificates', to='quiz.course'),
        ),
    ]