# Generated by Django 4.1 on 2024-01-12 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_alter_referrermentor_referrer_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvertisementImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='advertisement_images/')),
                ('desc', models.TextField(blank=True, null=True)),
            ],
        ),
    ]