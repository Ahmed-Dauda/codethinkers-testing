# Generated by Django 4.1.7 on 2023-04-14 06:01

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0002_rename_partdesc11_courses_partdesc1"),
    ]

    operations = [
        migrations.AddField(
            model_name="courses",
            name="img_img_partdesc2",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="image"
            ),
        ),
        migrations.AddField(
            model_name="courses",
            name="img_partdesc1",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="image"
            ),
        ),
    ]
