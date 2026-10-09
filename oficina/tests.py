from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Cliente, ItemOrcamento, MovimentacaoFinanceira, Orcamento, Peca, Servico


class FluxoFinanceiroEOficinaTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='qa', password='senha-segura')
        self.user.perfil.acesso_orcamentos = True
        self.user.perfil.save()
        self.client.force_login(self.user)
        self.cliente = Cliente.objects.create(nome='Cliente QA')

    def criar_os(self, status='OFICINA', total='100.00'):
        return Orcamento.objects.create(
            cliente=self.cliente,
            status=status,
            total=Decimal(total),
        )

    def get_dashboard(self):
        with patch('oficina.views.realizar_backup', create=True):
            return self.client.get(reverse('dashboard'))

    def test_dashboard_inclui_os_em_todas_as_etapas_apos_aprovacao(self):
        os_finalizada = self.criar_os(status='FINALIZADO', total='100.00')
        os_pendente = self.criar_os(status='PENDENTE', total='500.00')
        servico = Servico.objects.create(
            nome='Serviço QA',
            custo_mecanico=Decimal('40.00'),
            preco_venda=Decimal('100.00'),
        )
        ItemOrcamento.objects.create(
            orcamento=os_finalizada,
            tipo='SERVICO',
            servico=servico,
            nome=servico.nome,
            quantidade=1,
            preco_unitario=Decimal('100.00'),
            preco_total=Decimal('100.00'),
            custo_unitario=Decimal('40.00'),
        )

        response = self.get_dashboard()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['receita_bruta'], '100,00')
        self.assertEqual(response.context['receita_liquida'], '60,00')
        self.assertEqual(os_pendente.status, 'PENDENTE')

    def test_drilldown_liquido_usa_custo_snapshot_do_servico(self):
        os_finalizada = self.criar_os(status='FINALIZADO', total='100.00')
        servico = Servico.objects.create(nome='Serviço QA', custo_mecanico=Decimal('40.00'))
        ItemOrcamento.objects.create(
            orcamento=os_finalizada,
            tipo='SERVICO',
            servico=servico,
            nome=servico.nome,
            quantidade=1,
            preco_unitario=Decimal('100.00'),
            preco_total=Decimal('100.00'),
            custo_unitario=Decimal('40.00'),
        )

        response = self.client.get(reverse('dashboard_drilldown', args=['liquida']))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['dados'][0]['total'], 60.0)

    def test_custo_historico_permanece_apos_excluir_item_do_catalogo(self):
        os_finalizada = self.criar_os(status='FINALIZADO', total='100.00')
        peca = Peca.objects.create(nome='Peça QA', preco_custo=Decimal('35.00'), estoque=1)
        item = ItemOrcamento.objects.create(
            orcamento=os_finalizada,
            tipo='PECA',
            peca=peca,
            nome=peca.nome,
            quantidade=1,
            preco_unitario=Decimal('100.00'),
            preco_total=Decimal('100.00'),
            custo_unitario=Decimal('35.00'),
        )

        peca.delete()
        item.refresh_from_db()

        self.assertIsNone(item.peca_id)
        self.assertEqual(item.custo_unitario, Decimal('35.00'))
        response = self.get_dashboard()
        self.assertEqual(response.context['receita_liquida'], '65,00')

    def test_finalizar_os_nao_registra_recebimento_automaticamente(self):
        os_ = self.criar_os(status='TESTANDO')

        response = self.client.post(
            reverse('alterar_status_pedido', args=[os_.id]),
            {'status': 'FINALIZADO'},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(os_.pagamentos.count(), 0)

    def test_faturamento_explicito_nao_duplica_pagamento(self):
        os_ = self.criar_os(status='TESTANDO')

        for _ in range(2):
            response = self.client.post(
                reverse('faturar_orcamento', args=[os_.id]),
                {'forma_pagamento': 'PIX'},
            )
            self.assertEqual(response.status_code, 302)

        self.assertEqual(os_.pagamentos.count(), 1)
        pagamento = os_.pagamentos.get()
        self.assertEqual(pagamento.forma_pagamento, 'PIX')
        self.assertEqual(pagamento.status, 'PAGO')
        os_.refresh_from_db()
        self.assertEqual(os_.status, 'FINALIZADO')

    def test_aprovar_os_nao_baixa_estoque_mais_de_uma_vez(self):
        os_ = self.criar_os(status='PENDENTE')
        peca = Peca.objects.create(nome='Peça QA', preco_custo=Decimal('20.00'), estoque=3)
        ItemOrcamento.objects.create(
            orcamento=os_,
            tipo='PECA',
            peca=peca,
            nome=peca.nome,
            quantidade=1,
            preco_unitario=Decimal('30.00'),
            preco_total=Decimal('30.00'),
            custo_unitario=Decimal('20.00'),
        )

        for _ in range(2):
            self.client.post(reverse('aprovar_orcamento', args=[os_.id]))

        peca.refresh_from_db()
        os_.refresh_from_db()
        self.assertEqual(peca.estoque, 2)
        self.assertEqual(os_.status, 'APROVADO')

    def test_rota_de_movimentacao_financeira_exige_login(self):
        self.client.logout()

        response = self.client.post(
            reverse('nova_movimentacao'),
            {
                'tipo': 'RECEITA',
                'descricao': 'Acesso anônimo',
                'valor': '10.00',
                'data_vencimento': '2026-10-09',
                'status': 'PAGO',
                'forma_pagamento': 'PIX',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(MovimentacaoFinanceira.objects.count(), 0)

    def test_financeiro_usa_data_do_pagamento_e_nao_cria_recebimento_falso(self):
        from datetime import timedelta
        from django.utils import timezone

        os_finalizada = self.criar_os(status='FINALIZADO', total='100.00')
        data_pagamento = timezone.localdate()
        movimentacao = MovimentacaoFinanceira.objects.create(
            tipo='RECEITA',
            descricao='Recebimento com vencimento anterior',
            valor=Decimal('25.00'),
            data_vencimento=data_pagamento - timedelta(days=40),
            data_pagamento=data_pagamento,
            status='PAGO',
            forma_pagamento='PIX',
        )

        response = self.client.get(reverse('lista_financeiro'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['receitas'], Decimal('25.00'))
        self.assertContains(response, 'Recebimento com vencimento anterior')
        self.assertFalse(os_finalizada.pagamentos.exists())
        self.assertEqual(MovimentacaoFinanceira.objects.count(), 1)
        self.assertEqual(movimentacao.data_pagamento, data_pagamento)
