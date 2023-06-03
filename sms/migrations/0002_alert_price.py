# Generated by Django 4.1.7 on 2023-06-01 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="alert",
            name="price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                default="20000",
                max_digits=10,
                max_length=225,
                null=True,
            ),
        ),
    ]