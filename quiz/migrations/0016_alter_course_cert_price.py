# Generated by Django 4.1 on 2023-10-13 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0015_course_cert_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='cert_price',
            field=models.DecimalField(blank=True, decimal_places=0, default='1000', max_digits=10, max_length=225, null=True),
        ),
    ]