# Generated by Django 4.2.11 on 2024-06-24 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('depo', '0008_outgoingmaterial_production_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outgoingmaterial',
            name='production_order',
        ),
    ]
