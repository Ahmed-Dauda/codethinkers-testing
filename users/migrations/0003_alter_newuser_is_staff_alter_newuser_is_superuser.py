# Generated by Django 4.1 on 2023-12-13 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_referral_code_newuser_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]