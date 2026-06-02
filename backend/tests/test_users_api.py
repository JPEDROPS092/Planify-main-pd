from django.urls import reverse

from users.models import User
from tests.tenant_base import SuperuserAPITestCase


class UserAPITests(SuperuserAPITestCase):
    def test_create_user(self):
        url = reverse('user-list')
        data = {
            'email': 'user1@planify.com',
            'username': 'user1',
            'full_name': 'Usuário Um',
            'role': 'TEAM_MEMBER',
            'password': 'teste1234',
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
        # Sem credencial JWT, o PermissionMiddleware deve barrar com 401.
        self.client.credentials()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
