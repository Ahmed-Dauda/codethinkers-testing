# Generated by Django 3.2.8 on 2022-01-15 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0004_course_links_topics'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='course_link',
            field=models.URLField(blank=True, max_length=225, null=True),
        ),
    ]
