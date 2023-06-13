# Generated by Django 4.1.7 on 2023-06-11 18:42

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0033_remove_courses_course_desc_remove_courses_desc_home_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="courses",
            name="course_desc",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="courses",
            name="desc_home",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
    ]