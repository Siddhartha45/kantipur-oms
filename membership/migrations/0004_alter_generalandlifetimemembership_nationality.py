# Generated by Django 4.2.7 on 2023-12-05 07:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("membership", "0003_generalandlifetimemembership_created_by_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="generalandlifetimemembership",
            name="nationality",
            field=models.CharField(max_length=2),
        ),
    ]