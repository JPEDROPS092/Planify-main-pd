from datetime import date, timedelta

from django.urls import reverse

from projects.models import Projeto
from costs.models import OrcamentoProjeto
from tests.tenant_base import TenantAPITestCase


class CostAPITests(TenantAPITestCase):
    def setUp(self):
        super().setUp()
        self.project = Projeto.objects.create(
            titulo='Projeto Custo',
            descricao='Teste',
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=10),
            status='PLANEJADO',
            prioridade='MEDIA',
            criado_por=self.user,
        )

    def test_create_project_budget(self):
        url = reverse('orcamentoprojeto-list')
        data = {
            'projeto': self.project.id,
            'valor_total': 10000.0,
            'observacoes': 'Orçamento inicial',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(OrcamentoProjeto.objects.filter(observacoes='Orçamento inicial').exists())

    def test_list_project_budgets(self):
        url = reverse('orcamentoprojeto-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
