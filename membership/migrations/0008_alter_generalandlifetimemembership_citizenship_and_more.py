# Generated by Django 4.2.7 on 2023-12-05 08:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("membership", "0007_alter_generalandlifetimemembership_phd_country"),
    ]

    operations = [
        migrations.AlterField(
            model_name="generalandlifetimemembership",
            name="citizenship",
            field=models.ImageField(upload_to="general_and_lifetime_documents"),
        ),
        migrations.AlterField(
            model_name="generalandlifetimemembership",
            name="masters_document",
            field=models.ImageField(upload_to="general_and_lifetime_documents"),
        ),
        migrations.AlterField(
            model_name="generalandlifetimemembership",
            name="pp_photo",
            field=models.ImageField(upload_to="general_and_lifetime_documents"),
        ),
    ]
