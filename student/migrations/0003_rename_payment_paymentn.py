# Generated by Django 4.1 on 2023-07-23 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0001_initial"),
        ("users", "0002_profile_status_type"),
        ("student", "0002_payment_payment_course"),
    ]

    operations = [
        migrations.RenameModel(old_name="Payment", new_name="PaymentN",),
    ]
