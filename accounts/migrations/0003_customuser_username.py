# Generated by Django 4.2.7 on 2023-12-01 18:50

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_remove_customuser_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="username",
            field=models.CharField(
                default="ss",
                error_messages={"unique": "A user with that username already exists."},
                help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                max_length=150,
                unique=True,
                validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                verbose_name="username",
            ),
            preserve_default=False,
        ),
    ]
