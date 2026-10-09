from django.db import migrations, models


def snapshot_catalog_costs(apps, schema_editor):
    ItemOrcamento = apps.get_model('oficina', 'ItemOrcamento')
    for item in ItemOrcamento.objects.select_related('peca', 'servico').iterator():
        if item.tipo == 'PECA' and item.peca_id:
            item.custo_unitario = item.peca.preco_custo
        elif item.tipo == 'SERVICO' and item.servico_id:
            item.custo_unitario = item.servico.custo_mecanico
        item.save(update_fields=['custo_unitario'])


class Migration(migrations.Migration):

    dependencies = [
        ('oficina', '0004_cliente_arquivado_orcamento_arquivado_peca_arquivado_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemorcamento',
            name='custo_unitario',
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                help_text='Custo unitário registrado na criação do item',
                max_digits=10,
            ),
        ),
        migrations.RunPython(snapshot_catalog_costs, migrations.RunPython.noop),
    ]
