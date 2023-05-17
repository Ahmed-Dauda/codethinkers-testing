# Generated by Django 4.1.7 on 2023-05-15 13:17

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0003_alter_courses_categories"),
    ]

    operations = [
        migrations.AddField(
            model_name="courses",
            name="course_logo",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="course_logo"
            ),
        ),
        migrations.AddField(
            model_name="courses",
            name="course_owner",
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AddField(
            model_name="courses",
            name="course_type",
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
    ]