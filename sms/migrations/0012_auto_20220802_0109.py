# Generated by Django 3.1.4 on 2022-08-02 00:09

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0011_auto_20220802_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topics',
            name='student_activity',
            field=tinymce.models.HTMLField(null=True),
        ),
    ]
