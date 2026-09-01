
@login_required
def detalhe_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    # Mostra historico de orcamentos
    orcamentos = cliente.orcamentos.filter(arquivado=False).order_by('-criado_em')
    return render(request, 'cliente_detail.html', {'cliente': cliente, 'orcamentos': orcamentos})

@login_required
def exportar_historico_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    orcamentos = cliente.orcamentos.filter(arquivado=False).order_by('-criado_em')
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = f'historico_{cliente.nome.replace(" ", "_")}.xlsx'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Historico'

    columns = ['ID', 'Data', 'Status', 'Valor Pecas', 'Valor Servicos', 'Valor Total']
    worksheet.append(columns)

    for orc in orcamentos:
        worksheet.append([
            orc.id,
            orc.criado_em.strftime('%d/%m/%Y %H:%M'),
            orc.get_status_display(),
            orc.total_pecas,
            orc.total_mao_de_obra,
            orc.total
        ])

    workbook.save(response)
    return response
