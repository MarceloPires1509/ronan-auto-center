from django.http import HttpResponse
import openpyxl
from .models import Configuracao

@login_required
def configuracoes(request):
    if not request.user.perfil.acesso_configuracoes:
        messages.error(request, 'Você não tem permissão para acessar as configurações.')
        return redirect('dashboard')
        
    config, created = Configuracao.objects.get_or_create(id=1)
    usuarios = User.objects.all().select_related('perfil')
    
    if request.method == 'POST' and 'salvar_dados' in request.POST:
        config.nome_loja = request.POST.get('nome_loja')
        config.telefone = request.POST.get('telefone')
        config.endereco_completo = request.POST.get('endereco_completo')
        if 'logo' in request.FILES:
            config.logo = request.FILES['logo']
        config.save()
        messages.success(request, 'Configurações salvas com sucesso!')
        return redirect('configuracoes')
        
    if request.method == 'POST' and 'salvar_permissoes' in request.POST:
        user_id = request.POST.get('user_id')
        usuario_alvo = User.objects.get(id=user_id)
        perfil = usuario_alvo.perfil
        perfil.acesso_clientes = request.POST.get('acesso_clientes') == 'on'
        perfil.acesso_estoque = request.POST.get('acesso_estoque') == 'on'
        perfil.acesso_servicos = request.POST.get('acesso_servicos') == 'on'
        perfil.acesso_orcamentos = request.POST.get('acesso_orcamentos') == 'on'
        perfil.acesso_configuracoes = request.POST.get('acesso_configuracoes') == 'on'
        perfil.save()
        messages.success(request, f'Permissões de {usuario_alvo.first_name} atualizadas!')
        return redirect('configuracoes')
        
    return render(request, 'configuracoes.html', {'config': config, 'usuarios': usuarios})

@login_required
def exportar_orcamentos_excel(request):
    if not request.user.perfil.acesso_orcamentos:
        return redirect('dashboard')
        
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="orcamentos.xlsx"'

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Orçamentos'

    # Headers
    columns = ['ID', 'Cliente', 'Data', 'Status', 'Valor Peças', 'Valor Serviços', 'Valor Total']
    worksheet.append(columns)

    # Data
    for orc in Orcamento.objects.all().order_by('-data_criacao'):
        worksheet.append([
            orc.id,
            orc.cliente.nome if orc.cliente else 'Não Informado',
            orc.data_criacao.strftime('%d/%m/%Y %H:%M'),
            orc.get_status_display(),
            orc.total_pecas,
            orc.total_servicos,
            orc.total_geral
        ])

    workbook.save(response)
    return response
