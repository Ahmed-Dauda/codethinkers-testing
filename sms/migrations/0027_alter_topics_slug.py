# Generated by Django 4.1 on 2022-08-06 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0026_alter_topics_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="topics", name="slug", field=models.SlugField(unique=True),
        ),
    ]
