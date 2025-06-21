from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User, UserProfile
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.test import override_settings

# Desabilitar o middleware de permissões para os testes
@override_settings(MIDDLEWARE=[
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users.middleware.PermissionMiddleware',  # Incluir o middleware para testes realistas
])
class UserAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email='admin@planify.com',
            username='admin',
            full_name='Administrador',
            password='admin123',
        )
        self.regular_user = User.objects.create_user(
            email='user@planify.com',
            username='user',
            full_name='Usuário Regular',
            password='user123',
            role='TEAM_MEMBER'
        )
        self.client = APIClient()
    
    def authenticate_user(self, username, password):
        """Helper para autenticar usuário e retornar token"""
        login_url = reverse('login')
        login_data = {
            'username': username,
            'password': password
        }
        response = self.client.post(login_url, login_data, format='json')
        if response.status_code == 200:
            access_token = response.data['access']
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
            return access_token
        return None

    def test_create_user(self):
        """Teste de criação de usuário (apenas admins)"""
        self.client.force_authenticate(user=self.admin)
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
        """Teste de listagem de usuários"""
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Verificar se há pelo menos 2 usuários (admin e regular_user)
        self.assertGreaterEqual(len(response.data['results']), 2)

    def test_get_user_detail(self):
        """Teste de detalhes do usuário"""
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-detail', kwargs={'pk': self.regular_user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'user')

    def test_update_user(self):
        """Teste de atualização de usuário"""
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-detail', kwargs={'pk': self.regular_user.pk})
        data = {
            'full_name': 'Usuário Atualizado',
            'role': 'PROJECT_MANAGER'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.regular_user.refresh_from_db()
        self.assertEqual(self.regular_user.full_name, 'Usuário Atualizado')
        self.assertEqual(self.regular_user.role, 'PROJECT_MANAGER')

    def test_login(self):
        """Teste de login"""
        url = reverse('login')
        data = {
            'username': 'admin',
            'password': 'admin123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_credentials(self):
        """Teste de login com credenciais inválidas"""
        url = reverse('login')
        data = {
            'username': 'admin',
            'password': 'senha_errada'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_user_me(self):
        """Teste do endpoint /users/me/"""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('user-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'user')

    def test_change_password(self):
        """Teste de mudança de senha"""
        # Fazer login com usuário regular para obter token
        login_url = reverse('login')
        login_data = {
            'username': 'user',
            'password': 'user123'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        access_token = login_response.data['access']
        
        # Usar token para autenticação
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        url = reverse('user-change-password')
        data = {
            'old_password': 'user123',
            'new_password': 'newpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        
        # Verificar se a nova senha funciona
        user = authenticate(username='user', password='newpassword123')
        self.assertIsNotNone(user)

    def test_user_permissions_unauthorized(self):
        """Teste de permissões sem autenticação"""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_user_permissions_non_admin(self):
        """Teste de permissões com usuário não-admin"""
        # Fazer login com usuário regular para obter token
        login_url = reverse('login')
        login_data = {
            'username': 'user',
            'password': 'user123'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        access_token = login_response.data['access']
        
        # Usar token para autenticação
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        url = reverse('user-list')
        
        # Com o middleware de permissões ativo, usuários regulares não podem acessar a lista de usuários
        response = self.client.get(url)
        # Esperamos 403 porque o usuário regular não tem permissão USERS.VIEW
        self.assertEqual(response.status_code, 403)

    def test_user_activation(self):
        """Teste de ativação/desativação de usuário"""
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-deactivate', kwargs={'pk': self.regular_user.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.regular_user.refresh_from_db()
        self.assertFalse(self.regular_user.is_active)

        # Reativar
        url = reverse('user-activate', kwargs={'pk': self.regular_user.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.regular_user.refresh_from_db()
        self.assertTrue(self.regular_user.is_active)

    def test_user_profile(self):
        """Teste de perfil do usuário"""
        self.client.force_authenticate(user=self.regular_user)
        
        # Verificar se o perfil é criado automaticamente
        if not hasattr(self.regular_user, 'profile'):
            UserProfile.objects.create(user=self.regular_user)
        
        url = reverse('profile-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_jwt_token_authentication(self):
        """Teste de autenticação com token JWT"""
        # Primeiro fazer login para obter o token
        url = reverse('login')
        data = {
            'username': 'admin',
            'password': 'admin123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        access_token = response.data['access']
        
        # Usar o token para acessar um endpoint protegido
        self.client.logout()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_token_refresh(self):
        """Teste de atualização de token"""
        # Primeiro fazer login para obter os tokens
        url = reverse('login')
        data = {
            'username': 'admin',
            'password': 'admin123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        refresh_token = response.data['refresh']
        
        # Usar o refresh token para obter um novo access token
        url = reverse('token_refresh')
        data = {'refresh': refresh_token}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

    def test_logout(self):
        """Teste de logout"""
        # Primeiro fazer login para obter o token
        url = reverse('login')
        data = {
            'username': 'admin',
            'password': 'admin123'
        }
        response = self.client.post(url, data, format='json')
        access_token = response.data['access']
        
        # Fazer logout
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
