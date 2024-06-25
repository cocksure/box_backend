# Generated by Django 4.2.11 on 2024-06-19 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0006_remove_materialtype_queue'),
        ('depo', '0003_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='incoming',
            options={'verbose_name': 'Приход', 'verbose_name_plural': 'Приходы'},
        ),
        migrations.AlterModelOptions(
            name='incomingmaterial',
            options={'verbose_name': 'Материал прихода', 'verbose_name_plural': 'Материалы прихода'},
        ),
        migrations.AlterField(
            model_name='incoming',
            name='contract_number',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Номер контракта'),
        ),
        migrations.AlterField(
            model_name='incoming',
            name='data',
            field=models.DateField(verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='incoming',
            name='from_warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='incoming_from_warehouse', to='info.warehouse', verbose_name='От склада'),
        ),
        migrations.AlterField(
            model_name='incoming',
            name='incoming_type',
            field=models.CharField(blank=True, choices=[('Перемещение', 'Перемещение'), ('По накладной', 'По накладной')], max_length=150, null=True, verbose_name='Тип поступления'),
        ),
        migrations.AlterField(
            model_name='incoming',
            name='invoice',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Накладная'),
        ),
        migrations.AlterField(
            model_name='incoming',
            name='note',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Примечание'),
        ),
        migrations.AlterField(
            model_name='incoming',
            name='outgoing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='depo.outgoing', verbose_name='Исходящий'),
        ),
        migrations.AlterField(
            model_name='incoming',
            name='warehouse',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='incoming_warehouse', to='info.warehouse', verbose_name='Склад'),
        ),
        migrations.AlterField(
            model_name='incomingmaterial',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='incomingmaterial',
            name='comment',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='incomingmaterial',
            name='incoming',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='depo.incoming', verbose_name='Поступление'),
        ),
        migrations.AlterField(
            model_name='incomingmaterial',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.material', verbose_name='Материал'),
        ),
        migrations.AlterField(
            model_name='incomingmaterial',
            name='material_party',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Партия материала'),
        ),
    ]
