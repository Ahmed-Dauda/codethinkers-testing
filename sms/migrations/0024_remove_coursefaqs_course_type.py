# Generated by Django 4.1.7 on 2023-06-09 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0023_coursefaqs_course_type"),
    ]

    operations = [
        migrations.RemoveField(model_name="coursefaqs", name="course_type",),
    ]
