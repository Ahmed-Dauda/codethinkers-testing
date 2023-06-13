# Generated by Django 4.1.7 on 2023-06-11 19:52

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0036_alter_courses_course_desc_alter_courses_desc_home"),
    ]

    operations = [
        migrations.CreateModel(
            name="CourseLearnerReviews",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=225, null=True)),
                (
                    "desc",
                    tinymce.models.HTMLField(blank=True, max_length=500, null=True),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "courses",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sms.courses",
                    ),
                ),
            ],
        ),
    ]
