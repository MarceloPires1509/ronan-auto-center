from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/novo/', views.novo_cliente, name='novo_cliente'),
    path('clientes/excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),
    
    path('pecas/', views.lista_pecas, name='lista_pecas'),
    path('pecas/nova/', views.nova_peca, name='nova_peca'),
    path('pecas/excluir/<int:id>/', views.excluir_peca, name='excluir_peca'),
    
    path('servicos/', views.lista_servicos, name='lista_servicos'),
    path('servicos/novo/', views.novo_servico, name='novo_servico'),
    path('servicos/excluir/<int:id>/', views.excluir_servico, name='excluir_servico'),
    
    path('orcamentos/', views.lista_orcamentos, name='lista_orcamentos'),
    path('orcamentos/novo/', views.novo_orcamento, name='novo_orcamento'),
    path('orcamentos/excluir/<int:id>/', views.excluir_orcamento, name='excluir_orcamento'),
    path('orcamentos/aprovar/<int:id>/', views.aprovar_orcamento, name='aprovar_orcamento'),
    path('orcamentos/imprimir/<int:id>/', views.imprimir_orcamento, name='imprimir_orcamento'),
]
