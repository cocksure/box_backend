# Generated by Django 4.2.11 on 2024-05-22 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("info", "0005_materialtype_queue"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="materialtype",
            name="queue",
        ),
    ]
