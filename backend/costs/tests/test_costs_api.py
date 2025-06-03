from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User,UserManager
from projects.models import Projeto
from costs.models import OrcamentoProjeto
from datetime import date, timedelta
from typing import cast  # Importar cast para dicas de tipo
class CostAPITests(APITestCase):
    def setUp(self):
        user_manager = cast(UserManager, User.objects)
        self.admin = user_manager.create_superuser(
            email='admin@planify.com',
            username='admin',
            full_name='Administrador',
            password='admin123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)
        self.projeto = Projeto.objects.create(
            name='Projeto Custo',
            description='Teste',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=10),
            status='PLANNED',
            priority='MEDIUM',
            created_by=self.admin
        )

    def test_create_project_budget(self):
        url = reverse('orcamentoprojeto-list')
        data = {
            'projeto': self.projeto,  # Ensure 'projeto' is correctly set in the model
            'valor_total': 10000.0,
            'descricao': 'Orçamento inicial'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(OrcamentoProjeto.objects.filter(descricao='Orçamento inicial').exists())

    def test_list_project_budgets(self):
        url = reverse('orcamentoprojeto-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
