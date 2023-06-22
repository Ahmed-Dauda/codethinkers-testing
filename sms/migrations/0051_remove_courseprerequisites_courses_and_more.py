# Generated by Django 4.1.7 on 2023-06-18 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0050_courseprerequisites"),
    ]

    operations = [
        migrations.RemoveField(model_name="courseprerequisites", name="courses",),
        migrations.AddField(
            model_name="courses",
            name="prerequisite",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="courseprerequisites",
                to="sms.courseprerequisites",
            ),
        ),
    ]
