# Generated by Django 4.1 on 2023-07-25 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
        ("sms", "0003_remove_courses_student"),
    ]

    operations = [
        migrations.AddField(
            model_name="courses",
            name="student",
            field=models.ManyToManyField(
                blank=True, related_name="courses", to="users.profile"
            ),
        ),
    ]
