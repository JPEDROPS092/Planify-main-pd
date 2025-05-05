from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User
from projects.models import Project
from tasks.models import Task
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
        self.project = Project.objects.create(
            name='Projeto Tarefa',
            description='Teste',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=10),
            status='PLANNED',
            priority='MEDIUM',
            created_by=self.admin
        )

    def test_create_task(self):
        url = reverse('task-list')
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
        self.assertTrue(Task.objects.filter(titulo='Tarefa Teste').exists())

    def test_list_tasks(self):
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
