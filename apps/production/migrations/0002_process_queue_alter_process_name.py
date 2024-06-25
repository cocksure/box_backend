# Generated by Django 4.2.11 on 2024-06-19 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='queue',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, verbose_name='Очеред'),
        ),
        migrations.AlterField(
            model_name='process',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Название'),
        ),
    ]