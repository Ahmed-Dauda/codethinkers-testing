# Generated by Django 4.1.7 on 2023-06-09 11:26

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0027_remove_coursefaqs_course_type_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="topics", name="img_tutorial",),
        migrations.AlterField(
            model_name="topics",
            name="img_topic",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="topic image"
            ),
        ),
    ]
