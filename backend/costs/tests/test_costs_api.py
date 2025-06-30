from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User
from projects.models import Project
from costs.models import OrcamentoProjeto, Custo
from datetime import date, timedelta

class CostAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email='admin@planify.com',
            username='admin',
            full_name='Administrador',
            password='admin123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)
        
        self.project = Project.objects.create(
            name='Projeto Custo',
            description='Teste',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=10),
            status='PLANNED',
            priority='MEDIUM',
            created_by=self.admin
        )
        
        # Criar um orçamento de projeto inicial para testes de detalhe, atualização e exclusão
        self.orcamento_projeto = OrcamentoProjeto.objects.create(
            projeto=self.project,
            valor_total=5000.0,
            observacoes='Orçamento para testes de CRUD'
        )

    def test_create_project_budget(self):
        """
        Teste para a criação de um novo orçamento de projeto.
        """
        url = reverse('orcamentoprojeto-list')
        data = {
            'projeto': self.project.id,
            'valor_total': 10000.0,
            'observacoes': 'Orçamento inicial'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(OrcamentoProjeto.objects.filter(observacoes='Orçamento inicial').exists())

    def test_list_project_budgets(self):
        """
        Teste para listar todos os orçamentos de projeto.
        """
        url = reverse('orcamentoprojeto-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)

    def test_retrieve_project_budget(self):
        """
        Teste para recuperar os detalhes de um orçamento de projeto específico.
        """
        url = reverse('orcamentoprojeto-detail', kwargs={'pk': self.orcamento_projeto.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['valor_total'], str(self.orcamento_projeto.valor_total))
        self.assertEqual(response.data['observacoes'], self.orcamento_projeto.observacoes)

    def test_update_project_budget(self):
        """
        Teste para atualizar um orçamento de projeto existente.
        """
        url = reverse('orcamentoprojeto-detail', kwargs={'pk': self.orcamento_projeto.id})
        updated_data = {
            'valor_total': 7500.0,
            'observacoes': 'Orçamento revisado'
        }
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.orcamento_projeto.refresh_from_db()
        self.assertEqual(self.orcamento_projeto.valor_total, 7500.0)
        self.assertEqual(self.orcamento_projeto.observacoes, 'Orçamento revisado')

    def test_delete_project_budget(self):
        """
        Teste para excluir um orçamento de projeto.
        """
        url = reverse('orcamentoprojeto-detail', kwargs={'pk': self.orcamento_projeto.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204) # 204 No Content for successful deletion
        self.assertFalse(OrcamentoProjeto.objects.filter(id=self.orcamento_projeto.id).exists())

    def test_create_cost(self):
        """
        Teste para a criação de um novo custo (despesa).
        """
        url = reverse('custo-list')
        data = {
            'projeto': self.project.id,
            'tipo': 'MATERIAL',
            'descricao': 'Compra de materiais',
            'valor': 500.0,
            'data': date.today().isoformat()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Custo.objects.filter(descricao='Compra de materiais').exists())

    def test_list_costs(self):
        """
        Teste para listar todos os custos (despesas).
        """
        # Criar um custo para garantir que a lista não esteja vazia
        Custo.objects.create(
            projeto=self.project,
            tipo='VIAGEM',
            descricao='Despesas de viagem',
            valor=250.0,
            data=date.today()
        )
        url = reverse('custo-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)