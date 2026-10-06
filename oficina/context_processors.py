from .models import Configuracao, Peca
from django.db.models import F

def configuracao_global(request):
    config = Configuracao.objects.first()
    
    # Notificações de Estoque Baixo (quando estoque <= estoque_minimo)
    # Somente para usuários autenticados que têm permissão de estoque
    notificacoes_estoque = []
    if request.user.is_authenticated:
        if request.user.is_superuser or (hasattr(request.user, 'perfil') and request.user.perfil.acesso_estoque):
            # F usa o valor do outro campo
            pecas_baixo_estoque = Peca.objects.filter(estoque__lte=F('estoque_minimo'))
            notificacoes_estoque = pecas_baixo_estoque
            
    return {
        'config_global': config,
        'notificacoes_estoque': notificacoes_estoque,
        'qtd_notificacoes': len(notificacoes_estoque) if notificacoes_estoque else 0
    }
