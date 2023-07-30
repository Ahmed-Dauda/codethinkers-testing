# Generated by Django 4.1 on 2023-07-30 17:21

import cloudinary.models
from django.db import migrations, models
import student.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("sms", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Certificate",
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
                    "code",
                    models.CharField(
                        default=student.models.generate_certificate_code,
                        max_length=10,
                        unique=True,
                    ),
                ),
                ("holder", models.CharField(max_length=255, null=True)),
                ("issued_date", models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Designcert",
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
                    "design",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="image"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Logo",
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
                    "logo",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="image"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PartLogo",
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
                    "logo",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="image"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="signature",
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
                    "sign",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="image"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
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
                ("amount", models.PositiveBigIntegerField(null=True)),
                ("ref", models.CharField(max_length=250, null=True)),
                ("first_name", models.CharField(max_length=250, null=True)),
                ("last_name", models.CharField(max_length=200, null=True)),
                ("email", models.EmailField(max_length=254, null=True)),
                ("verified", models.BooleanField(default=False)),
                ("date_created", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "courses",
                    models.ManyToManyField(related_name="payments", to="sms.courses"),
                ),
            ],
        ),
    ]
