# Generated by Django 4.1 on 2022-08-12 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0011_remove_course_cert_note"),
    ]

    operations = [
        migrations.CreateModel(
            name="Certificate_note",
            fields=[
                ("note", models.TextField(blank=True, null=True)),
                ("desc", models.TextField(blank=True, null=True)),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
    ]
