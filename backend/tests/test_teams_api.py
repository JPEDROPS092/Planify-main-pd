from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User
from teams.models import Equipe

class TeamAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email='admin@planify.com',
            username='admin',
            full_name='Administrador',
            password='admin123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)

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
