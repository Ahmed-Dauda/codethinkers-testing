# Generated by Django 4.1.7 on 2023-06-09 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0026_remove_coursefaqs_faqs_courses_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="coursefaqs", name="course_type",),
        migrations.AddField(
            model_name="coursefaqs",
            name="faqs_courses",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="sms.courses"
            ),
        ),
    ]
