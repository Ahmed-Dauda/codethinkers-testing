# Generated by Django 4.1 on 2024-01-07 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_rename_ourse_student_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='course',
        ),
    ]