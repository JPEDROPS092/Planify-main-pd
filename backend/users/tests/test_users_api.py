from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User

class UserAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email='admin@planify.com',
            username='admin',
            full_name='Administrador',
            password='admin123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)

    def test_create_user(self):
        url = reverse('user-list')
        data = {
            'email': 'user1@planify.com',
            'username': 'user1',
            'full_name': 'Usuário Um',
            'role': 'TEAM_MEMBER',
            'password': 'teste1234'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username='user1').exists())

    def test_list_users(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_permissions(self):
        url = reverse('user-list')
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
