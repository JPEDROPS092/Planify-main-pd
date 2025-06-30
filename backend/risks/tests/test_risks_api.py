from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User
from projects.models import Project as Projeto  # Ensure correct model import
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
        
        self.project = Projeto.objects.create(
            name='Projeto Risco', # Use 'name' as per Project model in costs tests
            description='Teste',
            start_date=date.today(), # Use 'start_date' as per Project model in costs tests
            end_date=date.today() + timedelta(days=10), # Use 'end_date' as per Project model in costs tests
            status='PLANNED', # Use 'PLANNED' as per Project model in costs tests
            priority='MEDIUM', # Use 'MEDIUM' as per Project model in costs tests
            created_by=self.admin
        )
        
        # Criar um risco inicial para testes de detalhe, atualização e exclusão
        self.risco = Risco.objects.create(
            projeto=self.project,
            descricao='Risco Existente',
            probabilidade='MEDIA',
            impacto='BAIXO'
        )

    def test_create_risk(self):
        """
        Teste para a criação de um novo risco.
        """
        url = reverse('risco-list')
        data = {
            'projeto': self.project.id,
            'descricao': 'Risco Teste',
            'probabilidade': 'ALTA',
            'impacto': 'ALTO'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Risco.objects.filter(descricao='Risco Teste').exists())

    def test_list_risks(self):
        """
        Teste para listar todos os riscos.
        """
        url = reverse('risco-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)

    def test_retrieve_risk(self):
        """
        Teste para recuperar os detalhes de um risco específico.
        """
        url = reverse('risco-detail', kwargs={'pk': self.risco.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['descricao'], self.risco.descricao)
        self.assertEqual(response.data['probabilidade'], self.risco.probabilidade)
        self.assertEqual(response.data['impacto'], self.risco.impacto)

    def test_update_risk(self):
        """
        Teste para atualizar um risco existente.
        """
        url = reverse('risco-detail', kwargs={'pk': self.risco.id})
        updated_data = {
            'descricao': 'Risco Atualizado',
            'probabilidade': 'BAIXA',
            'impacto': 'MEDIO'
        }
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.risco.refresh_from_db()
        self.assertEqual(self.risco.descricao, 'Risco Atualizado')
        self.assertEqual(self.risco.probabilidade, 'BAIXA')
        self.assertEqual(self.risco.impacto, 'MEDIO')

    def test_delete_risk(self):
        """
        Teste para excluir um risco.
        """
        url = reverse('risco-detail', kwargs={'pk': self.risco.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204) # 204 No Content for successful deletion
        self.assertFalse(Risco.objects.filter(id=self.risco.id).exists())

    def test_create_risk_invalid_data(self):
        """
        Teste para tentar criar um risco com dados inválidos.
        """
        url = reverse('risco-list')
        data = {
            'projeto': self.project.id,
            'descricao': '',  # Descrição vazia é inválida
            'probabilidade': 'INVALIDA', # Probabilidade inválida
            'impacto': 'ALTO'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400) # Bad Request

    def test_update_risk_partial_data(self):
        """
        Teste para atualizar parcialmente um risco existente.
        """
        url = reverse('risco-detail', kwargs={'pk': self.risco.id})
        partial_data = {
            'impacto': 'ALTO'
        }
        response = self.client.patch(url, partial_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.risco.refresh_from_db()
        self.assertEqual(self.risco.impacto, 'ALTO')
        # A probabilidade deve permanecer a mesma, pois não foi alterada
        self.assertEqual(self.risco.probabilidade, 'MEDIA')