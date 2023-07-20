# Generated by Django 4.1.7 on 2023-07-20 09:58

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_profile_status_type"),
        ("sms", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FrequentlyAskQuestions",
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
                ("desc", models.TextField(blank=True, null=True)),
                (
                    "course_type",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated", models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Partners",
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
                ("title", models.CharField(max_length=100, null=True)),
                (
                    "img_partner",
                    cloudinary.models.CloudinaryField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="partner images",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(model_name="courses", name="course_desc",),
        migrations.RemoveField(model_name="courses", name="course_link",),
        migrations.RemoveField(model_name="courses", name="desc_home",),
        migrations.RemoveField(model_name="topics", name="coursedesc",),
        migrations.RemoveField(model_name="topics", name="img_tutorial",),
        migrations.AddField(
            model_name="alert",
            name="img_ebook",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="Ebook images"
            ),
        ),
        migrations.AddField(
            model_name="alert",
            name="price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                default="1500",
                max_digits=10,
                max_length=225,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="courses",
            name="prerequisites",
            field=models.ManyToManyField(blank=True, to="sms.courses"),
        ),
        migrations.AddField(
            model_name="courses",
            name="student",
            field=models.ManyToManyField(
                blank=True, related_name="courses", to="users.profile"
            ),
        ),
        migrations.AddField(
            model_name="topics",
            name="transcript",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="alert",
            name="content",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="blog",
            name="img_blog",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="blog image"
            ),
        ),
        migrations.AlterField(
            model_name="blogcomment",
            name="img_blogcomment",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="comment image"
            ),
        ),
        migrations.AlterField(
            model_name="courses",
            name="categories",
            field=models.ForeignKey(
                default=1,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="categories",
                to="sms.categories",
            ),
        ),
        migrations.AlterField(
            model_name="courses", name="desc", field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="courses",
            name="price",
            field=models.DecimalField(
                blank=True,
                decimal_places=0,
                default="20000",
                max_digits=10,
                max_length=225,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="courses",
            name="status_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Premium", "PREMIUM"),
                    ("Free", "FREE"),
                    ("Sponsored", "SPONSORED"),
                ],
                default="Free",
                max_length=225,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="gallery",
            name="gallery",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="gallery image"
            ),
        ),
        migrations.AlterField(
            model_name="topics",
            name="img_topic",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="topic image"
            ),
        ),
        migrations.AlterField(
            model_name="topics",
            name="slug",
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.CreateModel(
            name="Whatyouwilllearn",
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
                ("desc", models.TextField(blank=True, max_length=900, null=True)),
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
        migrations.CreateModel(
            name="Whatyouwillbuild",
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
                ("desc", models.CharField(blank=True, max_length=900, null=True)),
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
        migrations.CreateModel(
            name="Skillyouwillgain",
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
                ("title", models.CharField(blank=True, max_length=900, null=True)),
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
        migrations.CreateModel(
            name="ProfileStudent",
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
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="users.profile"
                    ),
                ),
            ],
        ),
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
                ("desc", models.TextField(blank=True, null=True)),
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
        migrations.CreateModel(
            name="CourseFrequentlyAskQuestions",
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
                ("desc", models.TextField(blank=True, null=True)),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
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
        migrations.CreateModel(
            name="CourseEnrolled",
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
                (
                    "students",
                    models.ManyToManyField(
                        related_name="enrolled_courses", to="sms.profilestudent"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CareerOpportunities",
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
                ("desc", tinymce.models.HTMLField(blank=True, null=True)),
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
        migrations.CreateModel(
            name="AboutCourseOwner",
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
                ("desc", models.TextField(blank=True, null=True)),
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
