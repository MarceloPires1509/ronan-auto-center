from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import openpyxl
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cliente, Peca, Servico, Orcamento, ItemOrcamento, Perfil, Configuracao
import json

from django.db.models import Sum, F
from django.utils import timezone

@login_required
def novo_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado.')
        else:
            user = User.objects.create_user(username=email, email=email, password=senha, first_name=nome)
            Perfil.objects.create(user=user, telefone=telefone)
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('dashboard')
            
    return render(request, 'usuario_form.html')

@login_required
def dashboard(request):
    agora = timezone.now()
    mes_atual = agora.month
    ano_atual = agora.year
    
    orcamentos_aprovados = Orcamento.objects.filter(status='APROVADO', criado_em__month=mes_atual, criado_em__year=ano_atual)
    receita_bruta = orcamentos_aprovados.aggregate(Sum('total'))['total__sum'] or 0.0
    
    # Receita Liquida simplificada: Receita Bruta - Custo das Peças e Serviços
    custo_total = 0
    for orc in orcamentos_aprovados:
        for item in orc.itens.all():
            if item.tipo == 'PECA' and item.peca:
                custo_total += float(item.peca.preco_custo) * item.quantidade
            elif item.tipo == 'SERVICO' and item.servico:
                custo_total += float(item.servico.custo_mecanico) * item.quantidade
                
    receita_liquida = float(receita_bruta) - custo_total
    
    orcamentos_pendentes = Orcamento.objects.filter(status='PENDENTE').count()
    pecas_baixo_estoque = Peca.objects.filter(estoque__lte=5).count()
    
    ultimos_orcamentos = Orcamento.objects.filter(arquivado=False).order_by('-criado_em')[:5]

    context = {
        'receita_bruta': "{:,.2f}".format(receita_bruta).replace(',', 'X').replace('.', ',').replace('X', '.'),
        'receita_liquida': "{:,.2f}".format(receita_liquida).replace(',', 'X').replace('.', ',').replace('X', '.'),
        'orcamentos_pendentes': orcamentos_pendentes,
        'pecas_baixo_estoque': pecas_baixo_estoque,
        'ultimos_orcamentos': ultimos_orcamentos
    }
    
    return render(request, 'dashboard.html', context)

# --- CLIENTES ---
@login_required
def lista_clientes(request):
    clientes = Cliente.objects.filter(arquivado=False).order_by('-criado_em')
    return render(request, 'clientes.html', {'clientes': clientes})

@login_required
def novo_cliente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        veiculo = request.POST.get('veiculo')
        placa = request.POST.get('placa')
        
        if nome:
            Cliente.objects.create(nome=nome, telefone=telefone, email=email, veiculo=veiculo, placa=placa)
            return redirect('lista_clientes')
            
    return render(request, 'cliente_form.html')

@login_required
def excluir_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
    return redirect('lista_clientes')

# --- PEÇAS (ESTOQUE) ---
@login_required
def lista_pecas(request):
    pecas = Peca.objects.filter(arquivado=False).order_by('nome')
    return render(request, 'pecas.html', {'pecas': pecas})

@login_required
def nova_peca(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco_custo = request.POST.get('preco_custo') or 0
        preco_venda = request.POST.get('preco_venda') or 0
        estoque = request.POST.get('estoque') or 0
        
        if nome:
            Peca.objects.create(
                nome=nome, 
                descricao=descricao, 
                preco_custo=str(preco_custo).replace(',', '.'), 
                preco_venda=str(preco_venda).replace(',', '.'), 
                estoque=estoque
            )
            return redirect('lista_pecas')
            
    return render(request, 'peca_form.html')

@login_required
def excluir_peca(request, id):
    peca = get_object_or_404(Peca, id=id)
    if request.method == 'POST':
        peca.delete()
    return redirect('lista_pecas')

# --- SERVIÇOS ---
@login_required
def lista_servicos(request):
    servicos = Servico.objects.filter(arquivado=False).order_by('nome')
    return render(request, 'servicos.html', {'servicos': servicos})

@login_required
def novo_servico(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        custo_mecanico = request.POST.get('custo_mecanico') or 0
        preco_venda = request.POST.get('preco_venda') or 0
        
        if nome:
            Servico.objects.create(
                nome=nome, 
                descricao=descricao, 
                custo_mecanico=str(custo_mecanico).replace(',', '.'), 
                preco_venda=str(preco_venda).replace(',', '.')
            )
            return redirect('lista_servicos')
            
    return render(request, 'servico_form.html')

@login_required
def excluir_servico(request, id):
    servico = get_object_or_404(Servico, id=id)
    if request.method == 'POST':
        servico.delete()
    return redirect('lista_servicos')

# --- ORÇAMENTOS E PDV ---
@login_required
def lista_orcamentos(request):
    orcamentos = Orcamento.objects.filter(arquivado=False).order_by('-criado_em')
    return render(request, 'orcamentos.html', {'orcamentos': orcamentos})

@login_required
def novo_orcamento(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        pecas_ids = request.POST.getlist('peca_id[]')
        pecas_qtds = request.POST.getlist('peca_qtd[]')
        servicos_ids = request.POST.getlist('servico_id[]')
        
        if cliente_id:
            cliente = get_object_or_404(Cliente, id=cliente_id)
            orcamento = Orcamento.objects.create(cliente=cliente)
            
            total_pecas = 0.0
            total_servicos = 0.0
            
            # Adiciona peças
            for pid, qtd_str in zip(pecas_ids, pecas_qtds):
                if pid:
                    peca = get_object_or_404(Peca, id=pid)
                    qtd = int(qtd_str) if qtd_str else 1
                    preco_total = float(peca.preco_venda) * qtd
                    ItemOrcamento.objects.create(
                        orcamento=orcamento, tipo='PECA', peca=peca, 
                        nome=peca.nome, quantidade=qtd, 
                        preco_unitario=peca.preco_venda, preco_total=preco_total
                    )
                    total_pecas += preco_total
            
            # Adiciona serviços
            for sid in servicos_ids:
                if sid:
                    servico = get_object_or_404(Servico, id=sid)
                    preco_total = float(servico.preco_venda)
                    ItemOrcamento.objects.create(
                        orcamento=orcamento, tipo='SERVICO', servico=servico,
                        nome=servico.nome, quantidade=1,
                        preco_unitario=servico.preco_venda, preco_total=preco_total
                    )
                    total_servicos += preco_total
                    
            orcamento.total_pecas = total_pecas
            orcamento.total_mao_de_obra = total_servicos
            orcamento.total = total_pecas + total_servicos
            orcamento.save()
            
            return redirect('lista_orcamentos')

    # GET request context
    clientes = Cliente.objects.filter(arquivado=False).order_by('nome')
    pecas = Peca.objects.filter(arquivado=False).order_by('nome')
    servicos = Servico.objects.filter(arquivado=False).order_by('nome')
    
    context = {
        'clientes': clientes,
        'pecas': pecas,
        'servicos': servicos,
    }
    return render(request, 'orcamento_form.html', context)

@login_required
def excluir_orcamento(request, id):
    orcamento = get_object_or_404(Orcamento, id=id)
    if request.method == 'POST':
        orcamento.delete()
    return redirect('lista_orcamentos')

@login_required
def aprovar_orcamento(request, id):
    orcamento = get_object_or_404(Orcamento, id=id)
    orcamento.status = 'APROVADO'
    orcamento.save()
    
    # Baixar estoque
    for item in orcamento.itens.filter(tipo='PECA'):
        if item.peca:
            item.peca.estoque -= item.quantidade
            item.peca.save()
            
    return redirect('lista_orcamentos')

@login_required
def imprimir_orcamento(request, id):
    orcamento = get_object_or_404(Orcamento, id=id)
    return render(request, 'orcamento_print.html', {'orcamento': orcamento})

from django.http import HttpResponse
import openpyxl
from .models import Configuracao

@login_required
def configuracoes(request):
    if not request.user.is_superuser and not request.user.perfil.acesso_configuracoes:
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
    for orc in Orcamento.objects.filter(arquivado=False).order_by('-criado_em'):
        worksheet.append([
            orc.id,
            orc.cliente.nome if orc.cliente else 'Não Informado',
            orc.criado_em.strftime('%d/%m/%Y %H:%M'),
            orc.get_status_display(),
            orc.total_pecas,
            orc.total_mao_de_obra,
            orc.total
        ])

    workbook.save(response)
    return response
@login_required
def arquivar_cliente(request, id):
    obj = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        obj.arquivado = True
        obj.save()
    return redirect('lista_clientes')

@login_required
def arquivar_peca(request, id):
    obj = get_object_or_404(Peca, id=id)
    if request.method == 'POST':
        obj.arquivado = True
        obj.save()
    return redirect('lista_pecas')

@login_required
def arquivar_servico(request, id):
    obj = get_object_or_404(Servico, id=id)
    if request.method == 'POST':
        obj.arquivado = True
        obj.save()
    return redirect('lista_servicos')

@login_required
def arquivar_orcamento(request, id):
    obj = get_object_or_404(Orcamento, id=id)
    if request.method == 'POST':
        obj.arquivado = True
        obj.save()
    return redirect('lista_orcamentos')


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
