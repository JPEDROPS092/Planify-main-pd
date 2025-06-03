from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User
from typing import cast
from communications.models import ChatMensagem

class CommunicationAPITests(APITestCase):
    user_manager = User.objects

    def setUp(self):
        from django.contrib.auth.models import UserManager  # Import UserManager
        user_manager = cast(UserManager, User.objects)
        self.admin = user_manager.create_superuser(
            email='admin@planify.com',
            username='admin',
            full_name='Administrador',
            password='admin123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)

    def test_send_message(self):
        url = reverse('chatmensagem-list')
        data = {
            'conteudo': 'Mensagem de teste',
            'remetente': self.admin.id
        }
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [201, 200])
        self.assertTrue(ChatMensagem.objects.filter(conteudo='Mensagem de teste').exists())

    def test_list_messages(self):
        url = reverse('chatmensagem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
