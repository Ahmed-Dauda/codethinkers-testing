# Generated by Django 4.1 on 2023-12-26 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0012_alter_ebookspayment_courses'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificatepayment',
            name='_cached_course_titles',
            field=models.TextField(blank=True, null=True),
        ),
    ]
