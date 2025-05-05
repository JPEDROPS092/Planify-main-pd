from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User
from projects.models import Project
from datetime import date, timedelta

class ProjectAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email='admin@planify.com',
            username='admin',
            full_name='Administrador',
            password='admin123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)

    def test_create_project(self):
        url = reverse('project-list')
        data = {
            'name': 'Projeto Teste',
            'description': 'Descrição',
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=30),
            'status': 'PLANNED',
            'priority': 'HIGH',
            'created_by': self.admin.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Project.objects.filter(name='Projeto Teste').exists())

    def test_list_projects(self):
        url = reverse('project-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
