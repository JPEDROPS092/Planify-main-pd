from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User
from communications.models import ChatMensagem
from projects.models import Project
from datetime import date, timedelta

class CommunicationAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email='admin@planify.com',
            username='admin',
            full_name='Administrador',
            password='admin123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)
        # Cria um projeto para associar à mensagem
        self.project = Project.objects.create(
            name='Projeto Teste Mensagem',
            description='Projeto para testar mensagens',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=10),
            status='PLANNED',
            priority='MEDIUM',
            created_by=self.admin
        )

    def test_send_message(self):
        url = reverse('chatmensagem-list')
        data = {
            'projeto': self.project.id,
            'texto': 'Mensagem de teste',
        }
        response = self.client.post(url, data, format='json')
        if response.status_code not in [200, 201]:
            print('Erro:', response.status_code, response.data)
        self.assertIn(response.status_code, [201, 200])
        self.assertTrue(ChatMensagem.objects.filter(texto='Mensagem de teste').exists())

    def test_list_messages(self):
        url = reverse('chatmensagem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
