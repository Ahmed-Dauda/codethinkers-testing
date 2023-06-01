# Generated by Django 4.1.7 on 2023-06-01 08:42

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Certificate_note",
            fields=[
                ("note", models.TextField(blank=True, null=True)),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                ("course_name", models.CharField(max_length=50, unique=True)),
                ("partdesc1", models.CharField(blank=True, max_length=300, null=True)),
                (
                    "img_partdesc1",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="image"
                    ),
                ),
                ("partdesc2", models.CharField(blank=True, max_length=229, null=True)),
                (
                    "img_partdesc2",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="image"
                    ),
                ),
                ("partdesc3", models.CharField(blank=True, max_length=225, null=True)),
                (
                    "signature",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="signature"
                    ),
                ),
                ("signby", models.CharField(blank=True, max_length=229, null=True)),
                (
                    "signby_portfolio",
                    models.CharField(blank=True, max_length=229, null=True),
                ),
                ("question_number", models.PositiveIntegerField()),
                ("total_marks", models.PositiveIntegerField()),
                ("pass_mark", models.PositiveIntegerField(null=True)),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated", models.DateTimeField(auto_now=True, null=True)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name="Result",
            fields=[
                ("marks", models.PositiveIntegerField()),
                ("date", models.DateTimeField(auto_now=True)),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated", models.DateTimeField(auto_now=True, null=True)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "exam",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="quiz.course"
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.profile"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                ("marks", models.PositiveIntegerField()),
                ("question", tinymce.models.HTMLField(blank=True, null=True)),
                (
                    "img_quiz",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="image"
                    ),
                ),
                ("option1", tinymce.models.HTMLField(max_length=200)),
                ("option2", tinymce.models.HTMLField(max_length=200)),
                ("option3", tinymce.models.HTMLField(max_length=200)),
                ("option4", tinymce.models.HTMLField(max_length=200)),
                (
                    "answer",
                    models.CharField(
                        choices=[
                            ("Option1", "Option1"),
                            ("Option2", "Option2"),
                            ("Option3", "Option3"),
                            ("Option4", "Option4"),
                        ],
                        max_length=200,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated", models.DateTimeField(auto_now=True, null=True)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="quiz.course"
                    ),
                ),
            ],
        ),
    ]
