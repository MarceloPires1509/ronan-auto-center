from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('usuarios/novo/', views.novo_usuario, name='novo_usuario'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
    path('orcamentos/exportar/', views.exportar_orcamentos_excel, name='exportar_orcamentos_excel'),
    path('orcamentos/exportar/pdf/', views.exportar_orcamentos_pdf, name='exportar_orcamentos_pdf'),
    
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/novo/', views.novo_cliente, name='novo_cliente'),
    path('clientes/excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),
    path('clientes/<int:id>/', views.detalhe_cliente, name='detalhe_cliente'),
    path('clientes/<int:id>/exportar/', views.exportar_historico_cliente, name='exportar_historico_cliente'),
    path('clientes/arquivar/<int:id>/', views.arquivar_cliente, name='arquivar_cliente'),
    
    path('pecas/', views.lista_pecas, name='lista_pecas'),
    path('pecas/nova/', views.nova_peca, name='nova_peca'),
    path('pecas/excluir/<int:id>/', views.excluir_peca, name='excluir_peca'),
    path('pecas/arquivar/<int:id>/', views.arquivar_peca, name='arquivar_peca'),
    
    path('servicos/', views.lista_servicos, name='lista_servicos'),
    path('servicos/novo/', views.novo_servico, name='novo_servico'),
    path('servicos/excluir/<int:id>/', views.excluir_servico, name='excluir_servico'),
    path('servicos/arquivar/<int:id>/', views.arquivar_servico, name='arquivar_servico'),
    
    path('orcamentos/', views.lista_orcamentos, name='lista_orcamentos'),
    path('orcamentos/novo/', views.novo_orcamento, name='novo_orcamento'),
    path('orcamentos/excluir/<int:id>/', views.excluir_orcamento, name='excluir_orcamento'),
    path('orcamentos/arquivar/<int:id>/', views.arquivar_orcamento, name='arquivar_orcamento'),
    path('orcamentos/aprovar/<int:id>/', views.aprovar_orcamento, name='aprovar_orcamento'),
    path('orcamentos/imprimir/<int:id>/', views.imprimir_orcamento, name='imprimir_orcamento'),
]
