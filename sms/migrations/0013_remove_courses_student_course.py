# Generated by Django 4.1 on 2023-10-29 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0012_courses_student_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courses',
            name='student_course',
        ),
    ]
