# Generated by Django 4.2.7 on 2023-12-30 18:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("membership", "0038_creategroups"),
    ]

    operations = [
        migrations.AlterField(
            model_name="creategroups",
            name="name",
            field=models.CharField(max_length=250, unique=True),
        ),
    ]