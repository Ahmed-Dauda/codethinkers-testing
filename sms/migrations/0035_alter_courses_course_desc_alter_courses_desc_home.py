# Generated by Django 4.1.7 on 2023-06-11 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0034_courses_course_desc_courses_desc_home"),
    ]

    operations = [
        migrations.AlterField(
            model_name="courses", name="course_desc", field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="courses", name="desc_home", field=models.TextField(null=True),
        ),
    ]
