# Generated by Django 4.1 on 2023-12-02 22:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_newuser_referral_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newuser',
            old_name='referral_code',
            new_name='code',
        ),
    ]
