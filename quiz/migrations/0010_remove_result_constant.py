# Generated by Django 4.1.7 on 2023-05-28 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0009_remove_course_constant"),
    ]

    operations = [
        migrations.RemoveField(model_name="result", name="constant",),
    ]
