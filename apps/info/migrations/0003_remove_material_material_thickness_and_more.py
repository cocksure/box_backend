# Generated by Django 4.2.11 on 2024-04-30 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("info", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="material",
            name="material_thickness",
        ),
        migrations.AlterField(
            model_name="material",
            name="code",
            field=models.CharField(
                blank=True, max_length=100, null=True, unique=True, verbose_name="Код"
            ),
        ),
    ]