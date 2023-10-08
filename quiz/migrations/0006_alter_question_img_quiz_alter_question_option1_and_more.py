# Generated by Django 4.1 on 2023-08-03 22:07

import cloudinary.models
from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0005_alter_question_option1_alter_question_option2_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="img_quiz",
            field=cloudinary.models.CloudinaryField(
                max_length=255, null=True, verbose_name="image"
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="option1",
            field=tinymce.models.HTMLField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="question",
            name="option2",
            field=tinymce.models.HTMLField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="question",
            name="option3",
            field=tinymce.models.HTMLField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="question",
            name="option4",
            field=tinymce.models.HTMLField(max_length=500, null=True),
        ),
    ]