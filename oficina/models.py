from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefone = models.CharField(max_length=20, blank=True, null=True)
    
    # Permissões
    acesso_clientes = models.BooleanField(default=True)
    acesso_estoque = models.BooleanField(default=True)
    acesso_servicos = models.BooleanField(default=True)
    acesso_orcamentos = models.BooleanField(default=True)
    acesso_configuracoes = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Configuracao(models.Model):
    nome_loja = models.CharField(max_length=255, default='Ronan Auto Center')
    endereco_completo = models.TextField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    
    def __str__(self):
        return self.nome_loja

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    veiculo = models.CharField(max_length=255, blank=True, null=True)
    placa = models.CharField(max_length=20, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    arquivado = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class Peca(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estoque = models.IntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)
    arquivado = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class Servico(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    custo_mecanico = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    criado_em = models.DateTimeField(auto_now_add=True)
    arquivado = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class Orcamento(models.Model):
    STATUS_CHOICES = (
        ('PENDENTE', 'Pendente'),
        ('APROVADO', 'Aprovado'),
        ('REJEITADO', 'Rejeitado'),
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='orcamentos')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    total_pecas = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_mao_de_obra = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    arquivado = models.BooleanField(default=False)

    def __str__(self):
        return f"Orçamento #{self.id} - {self.cliente.nome}"

class ItemOrcamento(models.Model):
    TIPO_CHOICES = (
        ('PECA', 'Peça'),
        ('SERVICO', 'Serviço'),
    )
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name='itens')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    peca = models.ForeignKey(Peca, on_delete=models.SET_NULL, null=True, blank=True)
    servico = models.ForeignKey(Servico, on_delete=models.SET_NULL, null=True, blank=True)
    nome = models.CharField(max_length=255)
    quantidade = models.IntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    preco_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantidade}x {self.nome}"

class Venda(models.Model):
    orcamento = models.OneToOneField(Orcamento, on_delete=models.SET_NULL, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_pagamento = models.CharField(max_length=50, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venda #{self.id}"


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
