# Generated by Django 4.1 on 2023-12-13 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_certificatepayment_f_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificatepayment',
            name='f_code',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]