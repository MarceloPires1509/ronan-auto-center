
@login_required
def restaurar_cliente(request, id):
    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, id=id)
        cliente.arquivado = False
        cliente.save()
        messages.success(request, 'Cliente restaurado com sucesso!')
    return redirect(reverse('lista_clientes') + '?arquivados=1')

@login_required
def restaurar_peca(request, id):
    if request.method == 'POST':
        peca = get_object_or_404(Peca, id=id)
        peca.arquivado = False
        peca.save()
        messages.success(request, 'Peça restaurada com sucesso!')
    return redirect(reverse('lista_pecas') + '?arquivados=1')

@login_required
def restaurar_servico(request, id):
    if request.method == 'POST':
        servico = get_object_or_404(Servico, id=id)
        servico.arquivado = False
        servico.save()
        messages.success(request, 'Serviço restaurado com sucesso!')
    return redirect(reverse('lista_servicos') + '?arquivados=1')
