# Generated by Django 3.2.9 on 2022-07-05 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pic/Teacher/')),
                ('address', models.CharField(max_length=40)),
                ('mobile', models.CharField(max_length=20)),
                ('status', models.BooleanField(default=False)),
                ('salary', models.PositiveIntegerField(null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
    ]
