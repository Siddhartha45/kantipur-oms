# Generated by Django 4.2.7 on 2023-12-08 04:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("membership", "0012_institutionalmembership_contact_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="generalandlifetimemembership",
            name="membership_no",
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
