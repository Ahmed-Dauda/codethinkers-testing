# Generated by Django 4.1 on 2024-02-10 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0021_rename_manyschools_course_schools'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='schools',
        ),
    ]