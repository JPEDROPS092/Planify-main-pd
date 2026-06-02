from django.urls import reverse

from teams.models import Equipe
from tests.tenant_base import TenantAPITestCase


class TeamAPITests(TenantAPITestCase):
    def test_create_team(self):
        url = reverse('equipe-list')
        data = {
            'nome': 'Equipe Teste',
            'descricao': 'Equipe para testes',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Equipe.objects.filter(nome='Equipe Teste').exists())

    def test_list_teams(self):
        url = reverse('equipe-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
