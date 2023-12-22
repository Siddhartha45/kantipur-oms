# Generated by Django 4.2.7 on 2023-12-22 17:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("membership", "0029_generalandlifetimemembership_membership_since"),
    ]

    operations = [
        migrations.AddField(
            model_name="generalandlifetimemembership",
            name="salutation",
            field=models.CharField(
                blank=True,
                choices=[
                    ("P", "Prof"),
                    ("D", "Dr"),
                    ("E", "Er"),
                    ("MR", "Mr"),
                    ("MS", "Ms"),
                ],
                max_length=2,
                null=True,
            ),
        ),
    ]