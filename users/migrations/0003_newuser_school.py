# Generated by Django 4.1 on 2024-01-09 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0011_alter_student_user'),
        ('users', '0002_profile_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='quiz.school'),
        ),
    ]
