from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Cliente

@csrf_exempt
def api_criar_cliente(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nome = data.get('nome')
            telefone = data.get('telefone', '')
            veiculo = data.get('veiculo', '')
            placa = data.get('placa', '')
            
            if not nome:
                return JsonResponse({'sucesso': False, 'erro': 'Nome é obrigatório.'})
                
            cliente = Cliente.objects.create(
                nome=nome,
                telefone=telefone,
                veiculo=veiculo,
                placa=placa
            )
            return JsonResponse({
                'sucesso': True,
                'cliente': {
                    'id': cliente.id,
                    'nome': cliente.nome,
                    'veiculo': cliente.veiculo,
                    'placa': cliente.placa
                }
            })
        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': str(e)})
    return JsonResponse({'sucesso': False, 'erro': 'Método não permitido.'})
