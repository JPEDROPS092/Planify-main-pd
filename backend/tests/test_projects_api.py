from datetime import date, timedelta

from django.urls import reverse

from projects.models import Projeto
from tests.tenant_base import TenantAPITestCase


class ProjectAPITests(TenantAPITestCase):
    def test_create_project(self):
        url = reverse('projects:projects-list')
        data = {
            'titulo': 'Projeto Teste',
            'descricao': 'Descrição',
            'data_inicio': date.today(),
            'data_fim': date.today() + timedelta(days=30),
            'status': 'PLANEJADO',
            'prioridade': 'ALTA',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Projeto.objects.filter(titulo='Projeto Teste').exists())

    def test_list_projects(self):
        url = reverse('projects:projects-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
