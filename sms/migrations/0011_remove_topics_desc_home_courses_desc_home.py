# Generated by Django 4.1.7 on 2023-03-12 11:26

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0010_topics_desc_home"),
    ]

    operations = [
        migrations.RemoveField(model_name="topics", name="desc_home",),
        migrations.AddField(
            model_name="courses",
            name="desc_home",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
    ]