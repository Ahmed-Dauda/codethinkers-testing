# Generated by Django 4.1 on 2023-11-09 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0013_remove_courses_student_course'),
        ('student', '0017_alter_certificatepayment_courses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificatepayment',
            name='courses',
            field=models.ManyToManyField(related_name='certificates', to='sms.courses'),
        ),
    ]
