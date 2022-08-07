# Generated by Django 3.1.4 on 2022-08-02 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20220728_0045'),
        ('sms', '0014_auto_20220802_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcomment',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='sms.blog'),
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
    ]
