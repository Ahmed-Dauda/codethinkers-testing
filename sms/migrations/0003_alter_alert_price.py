# Generated by Django 4.1.7 on 2023-06-01 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0002_alert_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="alert",
            name="price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                default="10000",
                max_digits=10,
                max_length=225,
                null=True,
            ),
        ),
    ]