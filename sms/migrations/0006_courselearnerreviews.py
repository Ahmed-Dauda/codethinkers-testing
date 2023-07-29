# Generated by Django 4.1 on 2023-07-29 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0005_delete_courselearnerreviews"),
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
                ("desc", models.TextField(null=True)),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "courses_review",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="courselearner",
                        to="sms.courses",
                    ),
                ),
            ],
        ),
    ]
