import os

with open('oficina/models.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Update Peca
old_peca = '''    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estoque = models.IntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)'''

new_peca = '''    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estoque = models.IntegerField(default=0)
    estoque_minimo = models.IntegerField(default=2)
    criado_em = models.DateTimeField(auto_now_add=True)'''

content = content.replace(old_peca, new_peca)

# Update Orcamento
old_orc = '''    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='orcamentos')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')'''

new_orc = '''    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='orcamentos')
    placa_veiculo = models.CharField(max_length=20, blank=True, null=True)
    modelo_veiculo = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')'''

content = content.replace(old_orc, new_orc)

# Add MovimentacaoFinanceira
movimentacao = '''
class MovimentacaoFinanceira(models.Model):
    TIPO_CHOICES = (
        ('RECEITA', 'Receita'),
        ('DESPESA', 'Despesa'),
    )
    STATUS_CHOICES = (
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PAGO')
    forma_pagamento = models.CharField(max_length=50, blank=True, null=True)
    orcamento = models.ForeignKey(Orcamento, on_delete=models.SET_NULL, null=True, blank=True, related_name='pagamentos')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.descricao} (R$ {self.valor})"
'''

if 'class MovimentacaoFinanceira' not in content:
    content += movimentacao

with open('oficina/models.py', 'w', encoding='utf-8') as f:
    f.write(content)
