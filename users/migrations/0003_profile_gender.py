# Generated by Django 3.2.9 on 2021-12-08 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20211207_0331'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Male', 'Male')], max_length=225, null=True),
        ),
    ]
