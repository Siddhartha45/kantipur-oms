# Generated by Django 4.2.7 on 2024-01-01 07:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "membership",
            "0041_remove_creategroups_mail_status_storemail_created_at_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="storemail",
            name="associated_groups",
            field=models.CharField(default="ss", max_length=255),
            preserve_default=False,
        ),
    ]