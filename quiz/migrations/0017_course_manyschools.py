# Generated by Django 4.1 on 2024-02-10 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0016_alter_school_logo_alter_school_principal_signature'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='manyschools',
            field=models.ManyToManyField(related_name='courses', to='quiz.school'),
        ),
    ]