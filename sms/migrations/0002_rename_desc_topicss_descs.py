# Generated by Django 3.2.8 on 2021-11-22 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topicss',
            old_name='desc',
            new_name='descs',
        ),
    ]
