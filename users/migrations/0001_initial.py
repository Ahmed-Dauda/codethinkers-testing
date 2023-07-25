# Generated by Django 4.1 on 2023-07-25 08:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="NewUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("username", models.CharField(blank=True, max_length=35)),
                ("phone_number", models.CharField(blank=True, max_length=254)),
                ("first_name", models.CharField(blank=True, max_length=254, null=True)),
                ("last_name", models.CharField(blank=True, max_length=254, null=True)),
                ("countries", models.CharField(blank=True, max_length=254, null=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("last_login", models.DateTimeField(blank=True, null=True)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={"db_table": "auth_user",},
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(blank=True, max_length=225)),
                ("first_name", models.CharField(blank=True, max_length=225, null=True)),
                ("last_name", models.CharField(blank=True, max_length=225, null=True)),
                (
                    "status_type",
                    models.CharField(
                        choices=[
                            ("Premium", "PREMIUM"),
                            ("Free", "FREE"),
                            ("Sponsored", "SPONSORED"),
                        ],
                        default="Free",
                        max_length=225,
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("Male", "Male"), ("Female", "Female")],
                        max_length=225,
                        null=True,
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=225, null=True),
                ),
                ("countries", models.CharField(blank=True, max_length=225, null=True)),
                (
                    "pro_img",
                    models.ImageField(blank=True, null=True, upload_to="profile"),
                ),
                ("bio", models.TextField(blank=True, max_length=600, null=True)),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
