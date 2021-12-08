# Generated by Django 3.2.9 on 2021-12-08 21:38

from django.db import migrations, models
import django.db.models.deletion
import hitcount.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=225, null=True, unique=True)),
                ('desc', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            bases=(models.Model, hitcount.models.HitCountMixin),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=225, null=True)),
                ('last_name', models.CharField(blank=True, max_length=225, null=True)),
                ('title', models.CharField(blank=True, max_length=225, null=True)),
                ('desc', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=225)),
                ('desc', models.TextField(default='')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sms.categories')),
            ],
        ),
        migrations.CreateModel(
            name='Topics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=225, null=True, unique=True)),
                ('objectives', models.TextField(blank=True, null=True)),
                ('descs', models.TextField(blank=True, null=True)),
                ('student_activity', models.TextField(blank=True, null=True)),
                ('evaluation', models.TextField(blank=True, null=True)),
                ('img_topic', models.ImageField(blank=True, null=True, upload_to='')),
                ('topics_url', models.CharField(blank=True, choices=[('https://t.me/joinchat/4F9VVjDPLzAwM2Q0', 'Beginners python_url'), ('https://t.me/joinchat/5CBRm0mlq5VlZmE0', 'Beginners html_url'), ('https://t.me/joinchat/8qkzp31B9EE1YjY0', 'Beginners statistic_url'), ('https://t.me/joinchat/xRjZ9vXkUx43NmY0', 'Beginners django_url'), ('https://t.me/joinchat/hgBXeiRmfDA1M2M0', 'Beginners sql_url'), ('https://t.me/joinchat/NF7h8BKK_vFjOTk8', 'Beginners javascripts_url')], max_length=500, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sms.categories')),
                ('courses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sms.courses')),
            ],
        ),
    ]
