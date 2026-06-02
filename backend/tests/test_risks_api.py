from datetime import date, timedelta

from django.urls import reverse

from projects.models import Projeto
from risks.models import Risco
from tests.tenant_base import TenantAPITestCase


class RiskAPITests(TenantAPITestCase):
    def setUp(self):
        super().setUp()
        self.project = Projeto.objects.create(
            titulo='Projeto Risco',
            descricao='Teste',
            data_inicio=date.today(),
            data_fim=date.today() + timedelta(days=10),
            status='PLANEJADO',
            prioridade='MEDIA',
            criado_por=self.user,
        )

    def test_create_risk(self):
        url = reverse('risco-list')
        data = {
            'projeto': self.project.id,
            'descricao': 'Risco Teste',
            'probabilidade': 'ALTA',
            'impacto': 'ALTO',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Risco.objects.filter(descricao='Risco Teste').exists())

    def test_list_risks(self):
        url = reverse('risco-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
