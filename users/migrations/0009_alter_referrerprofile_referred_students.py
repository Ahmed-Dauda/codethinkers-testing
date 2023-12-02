# Generated by Django 4.1 on 2023-12-01 23:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_referrerprofile_referred_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referrerprofile',
            name='referred_students',
            field=models.ManyToManyField(blank=True, related_name='referrer_profiles', to=settings.AUTH_USER_MODEL),
        ),
    ]