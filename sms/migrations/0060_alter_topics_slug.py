# Generated by Django 4.1.7 on 2023-06-19 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0059_alter_topics_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="topics",
            name="slug",
            field=models.SlugField(blank=True, null=True),
        ),
    ]
