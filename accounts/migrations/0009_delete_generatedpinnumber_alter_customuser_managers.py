# Generated by Django 4.1 on 2023-12-14 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_generatedpinnumber'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GeneratedPinNumber',
        ),
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
            ],
        ),
    ]
