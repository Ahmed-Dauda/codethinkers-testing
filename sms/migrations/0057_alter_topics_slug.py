# Generated by Django 4.1.7 on 2023-06-19 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0056_profilestudent_courseenrolled"),
    ]

    operations = [
        migrations.AlterField(
            model_name="topics",
            name="slug",
            field=models.SlugField(blank=True, null=True),
        ),
    ]
