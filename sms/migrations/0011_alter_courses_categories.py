# Generated by Django 4.1.7 on 2023-06-05 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0010_rename_img_ebook_partners_img_partner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="courses",
            name="categories",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="categories",
                to="sms.categories",
            ),
        ),
    ]