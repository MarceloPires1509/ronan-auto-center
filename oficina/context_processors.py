from .models import Configuracao

def configuracao_global(request):
    config = Configuracao.objects.first()
    return {'config_global': config}
