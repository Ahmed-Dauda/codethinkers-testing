# Generated by Django 4.1 on 2023-10-08 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0009_topics_completed_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='completedtopics',
            old_name='puser',
            new_name='user',
        ),
    ]
