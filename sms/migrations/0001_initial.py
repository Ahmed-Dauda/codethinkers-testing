# Generated by Django 4.1.7 on 2023-04-14 18:51

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion
import embed_video.fields
import hitcount.models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("users", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="Alert",
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
                ("content", models.TextField()),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Blog",
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
                ("poster", models.CharField(blank=True, max_length=225, null=True)),
                ("title", models.CharField(blank=True, max_length=225, null=True)),
                ("img_source", models.CharField(max_length=225, null=True)),
                ("slug", models.SlugField(unique=True)),
                (
                    "img_blog",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="image"
                    ),
                ),
                ("desc", tinymce.models.HTMLField(blank=True, null=True)),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.profile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Categories",
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
                    "name",
                    models.CharField(
                        blank=True, max_length=225, null=True, unique=True
                    ),
                ),
                ("desc", models.TextField(blank=True, null=True)),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "img_cat",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="image"
                    ),
                ),
            ],
            bases=(models.Model, hitcount.models.HitCountMixin),
        ),
        migrations.CreateModel(
            name="Comment",
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
                    "username",
                    models.CharField(
                        blank=True,
                        default="fff",
                        max_length=225,
                        null=True,
                        unique=True,
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, default="fff", max_length=225, null=True
                    ),
                ),
                ("last_name", models.CharField(blank=True, max_length=225, null=True)),
                ("title", models.CharField(blank=True, max_length=225, null=True)),
                (
                    "desc",
                    tinymce.models.HTMLField(blank=True, max_length=500, null=True),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated", models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Courses",
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
                    "img_course",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="image"
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=225, null=True)),
                ("desc", tinymce.models.HTMLField(blank=True, null=True)),
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
                ("desc_home", tinymce.models.HTMLField(blank=True, null=True)),
                ("course_desc", tinymce.models.HTMLField(blank=True, null=True)),
                ("course_link", models.URLField(blank=True, max_length=225, null=True)),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "categories",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="sms.categories"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Gallery",
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
                    "gallery",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="image"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Topics",
            fields=[
                ("title", models.CharField(blank=True, max_length=500, null=True)),
                ("slug", models.SlugField(max_length=500)),
                ("desc", tinymce.models.HTMLField(blank=True, null=True)),
                ("coursedesc", tinymce.models.HTMLField(blank=True, null=True)),
                (
                    "img_topic",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="image"
                    ),
                ),
                (
                    "img_tutorial",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="image"
                    ),
                ),
                ("video", embed_video.fields.EmbedVideoField(blank=True, null=True)),
                ("topics_url", models.CharField(blank=True, max_length=500, null=True)),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated", models.DateTimeField(auto_now=True, null=True)),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "categories",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="sms.categories"
                    ),
                ),
                (
                    "courses",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="sms.courses"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Blogcomment",
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
                ("name", models.CharField(max_length=100, null=True)),
                ("content", models.TextField()),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "img_blogcomment",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="image"
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="comments",
                        to="sms.blog",
                    ),
                ),
            ],
        ),
    ]
