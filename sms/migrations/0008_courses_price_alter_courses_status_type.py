# Generated by Django 4.1.7 on 2023-05-21 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0007_alter_courses_course_type_alter_courses_status_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="courses",
            name="price",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, max_length=225, null=True
            ),
        ),
        migrations.AlterField(
            model_name="courses",
            name="status_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("premium", "PREMIUM"),
                    ("free", "FREE"),
                    ("Sponsored", "SPONSORED"),
                ],
                default="premium",
                max_length=225,
                null=True,
            ),
        ),
    ]
