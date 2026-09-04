from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # PWA
    path('manifest.json', TemplateView.as_view(template_name='manifest.json', content_type='application/json'), name='manifest'),
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/javascript'), name='sw'),
    
    # Rotas padrão
    path('', views.dashboard, name='dashboard'),
    path('usuarios/novo/', views.novo_usuario, name='novo_usuario'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
    path('busca-placa/', views.busca_placa, name='busca_placa'),
    path('financeiro/', views.lista_financeiro, name='lista_financeiro'),
    path('financeiro/nova/', views.nova_movimentacao, name='nova_movimentacao'),
    path('pedidos/faturar/<int:id>/', views.faturar_orcamento, name='faturar_orcamento'),

    path('orcamentos/exportar/', views.exportar_orcamentos_excel, name='exportar_orcamentos_excel'),
    path('orcamentos/exportar/pdf/', views.exportar_orcamentos_pdf, name='exportar_orcamentos_pdf'),
    
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/novo/', views.novo_cliente, name='novo_cliente'),
    path('clientes/excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),
    path('clientes/<int:id>/', views.detalhe_cliente, name='detalhe_cliente'),
    path('clientes/<int:id>/exportar/', views.exportar_historico_cliente, name='exportar_historico_cliente'),
    path('clientes/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    
    path('pecas/', views.lista_pecas, name='lista_pecas'),
    path('pecas/nova/', views.nova_peca, name='nova_peca'),
    path('pecas/excluir/<int:id>/', views.excluir_peca, name='excluir_peca'),
    path('pecas/arquivar/<int:id>/', views.arquivar_peca, name='arquivar_peca'),
    path('pecas/restaurar/<int:id>/', views.restaurar_peca, name='restaurar_peca'),
    
    path('servicos/', views.lista_servicos, name='lista_servicos'),
    path('servicos/novo/', views.novo_servico, name='novo_servico'),
    path('servicos/excluir/<int:id>/', views.excluir_servico, name='excluir_servico'),
    path('servicos/arquivar/<int:id>/', views.arquivar_servico, name='arquivar_servico'),
    path('servicos/restaurar/<int:id>/', views.restaurar_servico, name='restaurar_servico'),
    
    path('orcamentos/', views.lista_orcamentos, name='lista_orcamentos'),
    path('orcamentos/novo/', views.novo_orcamento, name='novo_orcamento'),
    path('orcamentos/excluir/<int:id>/', views.excluir_orcamento, name='excluir_orcamento'),
    path('orcamentos/aprovar/<int:id>/', views.aprovar_orcamento, name='aprovar_orcamento'),
    
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('pedidos/status/<int:id>/', views.alterar_status_pedido, name='alterar_status_pedido'),
    path('orcamentos/imprimir/<int:id>/', views.imprimir_orcamento, name='imprimir_orcamento'),
]
