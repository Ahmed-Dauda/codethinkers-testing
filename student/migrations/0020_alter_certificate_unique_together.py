# Generated by Django 5.0.4 on 2024-08-26 09:31

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0026_update_verification_codes'),
        ('student', '0019_update_verification_codes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='certificate',
            unique_together={('user', 'course')},
        ),
    ]
