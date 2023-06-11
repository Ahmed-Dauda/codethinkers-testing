# Generated by Django 4.1.7 on 2023-06-08 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0017_remove_courses_course_link_courses_faqs_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="courses",
            name="faqs",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="sms.frequentlyaskquestions",
            ),
        ),
    ]