# Generated by Django 4.1 on 2023-12-01 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_profile_referral_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='referral_code',
            field=models.CharField(blank=True, max_length=225),
        ),
    ]