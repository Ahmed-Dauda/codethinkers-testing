# Generated by Django 3.2.9 on 2021-12-04 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_newuser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='country',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
