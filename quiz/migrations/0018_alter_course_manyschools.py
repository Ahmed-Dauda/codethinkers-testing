# Generated by Django 4.1 on 2024-02-10 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0017_course_manyschools'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='manyschools',
            field=models.ManyToManyField(blank=True, null=True, related_name='courses', to='quiz.school'),
        ),
    ]
