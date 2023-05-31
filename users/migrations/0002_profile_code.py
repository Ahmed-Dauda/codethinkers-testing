# Generated by Django 4.1.7 on 2023-05-31 16:48

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="code",
            field=models.CharField(
                default=users.models.generate_certificate_code,
                max_length=10,
                unique=True,
            ),
        ),
    ]