# Generated by Django 4.1 on 2024-01-12 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_newuser_student_class'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='school',
        ),
    ]