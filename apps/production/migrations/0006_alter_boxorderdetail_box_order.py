# Generated by Django 4.2.11 on 2024-06-21 04:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0005_productionorder_code_productionorder_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boxorderdetail',
            name='box_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='production.boxorder', verbose_name='Заказ коробки'),
        ),
    ]
