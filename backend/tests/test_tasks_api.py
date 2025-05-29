from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User
from projects.models import Projeto
from tasks.models import Tarefa
from datetime import date, timedelta

class TaskAPITests(APITestCase):
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
            nome='Projeto Tarefa',
            descricao='Teste',
            data_inicio=date.today(),
            data_termino=date.today() + timedelta(days=10),
            status='PLANEJADO',
            prioridade='MEDIA',
            criado_por=self.admin
        )

    def test_create_task(self):
        url = reverse('tarefa-list')
        data = {
            'titulo': 'Tarefa Teste',
            'descricao': 'Descrição de teste',
            'data_inicio': date.today(),
            'data_termino': date.today() + timedelta(days=5),
            'prioridade': 'MEDIA',
            'status': 'A_FAZER',
            'projeto': self.project.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Tarefa.objects.filter(titulo='Tarefa Teste').exists())

    def test_list_tasks(self):
        url = reverse('tarefa-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
