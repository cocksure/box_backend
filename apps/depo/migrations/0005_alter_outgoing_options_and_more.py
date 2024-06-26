# Generated by Django 4.2.11 on 2024-06-19 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0001_initial'),
        ('info', '0006_remove_materialtype_queue'),
        ('depo', '0004_alter_incoming_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='outgoing',
            options={'verbose_name': 'Расход', 'verbose_name_plural': 'Расходы'},
        ),
        migrations.AlterModelOptions(
            name='outgoingmaterial',
            options={'verbose_name': 'Материал расхода', 'verbose_name_plural': 'Материалы расхода'},
        ),
        migrations.AddField(
            model_name='outgoing',
            name='production_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='outgoings', to='production.productionorder'),
        ),
        migrations.AlterField(
            model_name='outgoing',
            name='code',
            field=models.CharField(editable=False, max_length=10, unique=True, verbose_name='Код'),
        ),
        migrations.AlterField(
            model_name='outgoing',
            name='data',
            field=models.DateField(verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='outgoing',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='outgoing',
            name='note',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Примечание'),
        ),
        migrations.AlterField(
            model_name='outgoing',
            name='outgoing_type',
            field=models.CharField(choices=[('расход', 'Расход'), ('продажа', 'Продажа'), ('перемешения', 'Перемещение')], default='перемешения', max_length=20, verbose_name='Тип исхода'),
        ),
        migrations.AlterField(
            model_name='outgoing',
            name='status',
            field=models.CharField(blank=True, choices=[('Принят', 'Принят'), ('Отклонен', 'Отклонен'), ('В ожидании', 'В ожидании')], default='В ожидании', max_length=20, null=True, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='outgoing',
            name='to_warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_to_warehouse', to='info.warehouse', verbose_name='К складу'),
        ),
        migrations.AlterField(
            model_name='outgoing',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_warehouse', to='info.warehouse', verbose_name='Склад'),
        ),
        migrations.AlterField(
            model_name='outgoingmaterial',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='outgoingmaterial',
            name='comment',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='outgoingmaterial',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.material', verbose_name='Материал'),
        ),
        migrations.AlterField(
            model_name='outgoingmaterial',
            name='material_party',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Партия материала'),
        ),
        migrations.AlterField(
            model_name='outgoingmaterial',
            name='outgoing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_materials', to='depo.outgoing', verbose_name='Исходящая поставка'),
        ),
    ]
