# Generated by Django 4.1 on 2023-12-02 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0018_alter_certificatepayment_courses'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificatepayment',
            name='referral_code',
            field=models.CharField(max_length=250, null=True),
        ),
    ]