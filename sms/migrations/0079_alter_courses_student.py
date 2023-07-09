# Generated by Django 4.1.7 on 2023-06-30 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_remove_profile_courses"),
        ("sms", "0078_alter_topics_desc"),
    ]

    operations = [
        migrations.AlterField(
            model_name="courses",
            name="student",
            field=models.ManyToManyField(
                blank=True, related_name="courses", to="users.profile"
            ),
        ),
    ]
