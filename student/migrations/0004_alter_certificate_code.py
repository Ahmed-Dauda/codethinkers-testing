# Generated by Django 4.1.7 on 2023-05-31 16:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("student", "0003_certificate_user_alter_certificate_code_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="certificate",
            name="code",
            field=models.CharField(default=uuid.uuid4, max_length=255, unique=True),
        ),
    ]