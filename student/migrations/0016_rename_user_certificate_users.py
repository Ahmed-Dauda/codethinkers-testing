# Generated by Django 5.0.4 on 2024-08-15 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0015_remove_certificate_code_remove_certificate_holder_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='certificate',
            old_name='user',
            new_name='users',
        ),
    ]
