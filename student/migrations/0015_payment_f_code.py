# Generated by Django 4.1 on 2023-12-26 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0014_remove_certificatepayment__cached_course_titles_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='f_code',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]