# Generated by Django 4.1 on 2023-07-28 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="courselearnerreviews",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
