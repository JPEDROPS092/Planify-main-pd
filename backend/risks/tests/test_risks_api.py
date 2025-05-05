from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User
from projects.models import Projeto
from risks.models import Risco
from datetime import date, timedelta

class RiskAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email='admin@planify.com',
            username='admin',
            full_name='Administrador',
            password='admin123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)
        self.projeto = Projeto.objects.create(
            name='Projeto Risco',
            description='Teste',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=10),
            status='PLANNED',
            priority='MEDIUM',
            created_by=self.admin
        )

    def test_create_risk(self):
        url = reverse('risco-list')
        data = {
            'projeto': self.projeto.id,
            'descricao': 'Risco Teste',
            'probabilidade': 'ALTA',
            'impacto': 'GRAVE'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Risco.objects.filter(descricao='Risco Teste').exists())

    def test_list_risks(self):
        url = reverse('risco-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
