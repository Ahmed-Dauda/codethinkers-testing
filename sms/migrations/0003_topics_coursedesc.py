# Generated by Django 4.1 on 2022-12-30 17:14

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0002_alter_topics_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="topics",
            name="coursedesc",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
    ]