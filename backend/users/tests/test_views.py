# users/tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import UserProfile, AccessProfile, Permission, UserAccessProfile
from typing import Dict, Any, TYPE_CHECKING
import json

User = get_user_model()

# Type checking imports for better IDE support
if TYPE_CHECKING:
    from users.models import User as UserModel
else:
    UserModel = User


class BaseAPITestCase(TestCase):
    """Classe base para testes de API"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Criar usuário administrador
        self.admin_user = User.objects.create(
            username='admin',
            email='admin@example.com',
            full_name='Admin User',
            role='ADMIN',
            is_staff=True
        )
        self.admin_user.set_password('AdminPass123!')
        self.admin_user.save()
        
        # Criar usuário comum
        self.regular_user = User.objects.create(
            username='user',
            email='user@example.com',
            full_name='Regular User',
            role='TEAM_MEMBER'
        )
        self.regular_user.set_password('UserPass123!')
        self.regular_user.save()
        
        # Criar perfis para os usuários
        UserProfile.objects.get_or_create(user=self.admin_user)
        UserProfile.objects.get_or_create(user=self.regular_user)
    
    def get_tokens_for_user(self, user) -> Dict[str, str]:
        """Gera tokens JWT para um usuário"""
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),  # type: ignore
        }
    
    def authenticate_user(self, user) -> Dict[str, str]:
        """Autentica um usuário no client"""
        tokens = self.get_tokens_for_user(user)
        # Type ignore for Django REST framework dynamic attribute
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')  # type: ignore
        return tokens


class AuthenticationViewsTest(BaseAPITestCase):
    """Testes para views de autenticação"""
    
    def test_login_success(self):
        """Testa login bem-sucedido"""
        url = '/api/auth/login/'
        data = {
            'username': 'admin',
            'password': 'AdminPass123!'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.json())
        self.assertIn('refresh', response.json())
    
    def test_login_invalid_credentials(self):
        """Testa login com credenciais inválidas"""
        url = reverse('users:auth:login')
        data = {
            'username': 'admin',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.json())
    
    def test_login_missing_credentials(self):
        """Testa login com credenciais faltando"""
        url = reverse('users:auth:login')
        data = {
            'username': 'admin'
            # senha faltando
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_inactive_user(self):
        """Testa login com usuário inativo"""
        self.regular_user.is_active = False
        self.regular_user.save()
        
        url = reverse('users:auth:login')
        data = {
            'username': 'user',
            'password': 'UserPass123!'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('desativada', response.json()['detail'])
    
    def test_login_locked_user(self):
        """Testa login com usuário bloqueado"""
        self.regular_user.is_locked = True  # type: ignore
        self.regular_user.save()
        
        url = reverse('users:auth:login')
        data = {
            'username': 'user',
            'password': 'UserPass123!'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('bloqueada', response.json()['detail'])
    
    def test_logout_success(self):
        """Testa logout bem-sucedido"""
        tokens = self.authenticate_user(self.regular_user)
        
        url = reverse('users:auth:logout')
        data = {
            'refresh': tokens['refresh']
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.json())
    
    def test_logout_without_token(self):
        """Testa logout sem token"""
        self.authenticate_user(self.regular_user)
        
        url = reverse('users:auth:logout')
        data = {}
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_token_refresh_success(self):
        """Testa refresh de token bem-sucedido"""
        tokens = self.get_tokens_for_user(self.regular_user)
        
        url = reverse('users:auth:token_refresh')
        data = {
            'refresh': tokens['refresh']
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.json())
    
    def test_token_refresh_invalid(self):
        """Testa refresh com token inválido"""
        url = reverse('users:auth:token_refresh')
        data = {
            'refresh': 'invalid.token.here'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserViewSetTest(BaseAPITestCase):
    """Testes para UserViewSet"""
    
    def test_list_users_as_admin(self):
        """Testa listagem de usuários como admin"""
        self.authenticate_user(self.admin_user)
        
        url = reverse('users:user-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        
        # Se a resposta for paginada, verificar 'results'
        if 'results' in response_data:
            self.assertEqual(len(response_data['results']), 2)  # admin + regular user
        else:
            self.assertEqual(len(response_data), 2)  # admin + regular user
    
    def test_list_users_as_regular_user(self):
        """Testa listagem de usuários como usuário comum"""
        self.authenticate_user(self.regular_user)
        
        url = reverse('users:user-list')
        response = self.client.get(url)
        
        # Usuário comum não deve ter permissão para listar usuários
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_retrieve_user_as_admin(self):
        """Testa obtenção de usuário específico como admin"""
        self.authenticate_user(self.admin_user)
        
        url = reverse('users:user-detail', kwargs={'pk': self.regular_user.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['username'], 'user')
    
    def test_create_user_as_admin(self):
        """Testa criação de usuário como admin"""
        self.authenticate_user(self.admin_user)
        
        url = reverse('users:user-list')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'full_name': 'New User',
            'password': 'NewPass123!',
            'role': 'TEAM_MEMBER'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_create_user_without_permission(self):
        """Testa criação de usuário sem permissão"""
        self.authenticate_user(self.regular_user)
        
        url = reverse('users:user-list')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'full_name': 'New User',
            'password': 'NewPass123!',
            'role': 'TEAM_MEMBER'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_user_as_admin(self):
        """Testa atualização de usuário como admin"""
        self.authenticate_user(self.admin_user)
        
        url = reverse('users:user-detail', kwargs={'pk': self.regular_user.pk})
        data = {
            'full_name': 'Updated User Name'
        }
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.regular_user.refresh_from_db()
        self.assertEqual(self.regular_user.full_name, 'Updated User Name')  # type: ignore
    
    def test_delete_user_as_admin(self):
        """Testa exclusão de usuário como admin"""
        self.authenticate_user(self.admin_user)
        
        url = reverse('users:user-detail', kwargs={'pk': self.regular_user.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.regular_user.pk).exists())
    
    def test_me_endpoint(self):
        """Testa endpoint para obter informações do usuário atual"""
        self.authenticate_user(self.regular_user)
        
        url = reverse('users:user-me')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['username'], 'user')
        self.assertEqual(response.json()['email'], 'user@example.com')
    
    def test_permissions_endpoint(self):
        """Testa endpoint para obter permissões do usuário"""
        self.authenticate_user(self.regular_user)
        
        url = reverse('users:user-permissions')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('role', response.json())
        self.assertIn('permissions', response.json())
        self.assertEqual(response.json()['role'], 'TEAM_MEMBER')
    
    def test_change_password(self):
        """Testa alteração de senha"""
        self.authenticate_user(self.regular_user)
        
        url = reverse('users:user-change-password')
        data = {
            'old_password': 'UserPass123!',
            'new_password': 'NewSecurePass123!'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se a senha foi alterada
        self.regular_user.refresh_from_db()
        self.assertTrue(self.regular_user.check_password('NewSecurePass123!'))
    
    def test_change_password_wrong_old_password(self):
        """Testa alteração de senha com senha atual incorreta"""
        self.authenticate_user(self.regular_user)
        
        url = reverse('users:user-change-password')
        data = {
            'old_password': 'WrongPassword',
            'new_password': 'NewSecurePass123!'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_reset_password_as_admin(self):
        """Testa reset de senha como admin"""
        self.authenticate_user(self.admin_user)
        
        url = reverse('users:user-reset-password', kwargs={'pk': self.regular_user.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se o usuário precisa alterar a senha
        profile = UserProfile.objects.get(user=self.regular_user)
        self.assertTrue(profile.password_change_required)
    
    def test_activate_user(self):
        """Testa ativação de usuário"""
        self.authenticate_user(self.admin_user)
        
        # Desativar usuário primeiro
        self.regular_user.is_active = False
        self.regular_user.save()
        
        url = reverse('users:user-activate', kwargs={'pk': self.regular_user.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.regular_user.refresh_from_db()
        self.assertTrue(self.regular_user.is_active)
    
    def test_deactivate_user(self):
        """Testa desativação de usuário"""
        self.authenticate_user(self.admin_user)
        
        url = reverse('users:user-deactivate', kwargs={'pk': self.regular_user.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.regular_user.refresh_from_db()
        self.assertFalse(self.regular_user.is_active)
    
    def test_unlock_user(self):
        """Testa desbloqueio de usuário"""
        self.authenticate_user(self.admin_user)
        
        # Bloquear usuário primeiro
        self.regular_user.is_locked = True  # type: ignore
        self.regular_user.failed_login_attempts = 5  # type: ignore
        self.regular_user.save()
        
        url = reverse('users:user-unlock', kwargs={'pk': self.regular_user.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.regular_user.refresh_from_db()
        self.assertFalse(self.regular_user.is_locked)  # type: ignore
        self.assertEqual(self.regular_user.failed_login_attempts, 0)  # type: ignore


class PermissionViewSetTest(BaseAPITestCase):
    """Testes para PermissionViewSet"""
    
    def setUp(self):
        super().setUp()
        self.access_profile = AccessProfile.objects.create(
            name='Test Profile',
            description='Profile for testing'
        )
    
    def test_list_permissions_as_admin(self):
        """Testa listagem de permissões como admin"""
        self.authenticate_user(self.admin_user)
        
        # Criar algumas permissões
        Permission.objects.create(
            access_profile=self.access_profile,
            module='PROJECTS',
            action='VIEW'
        )
        Permission.objects.create(
            access_profile=self.access_profile,
            module='PROJECTS',
            action='CREATE'
        )
        
        url = reverse('users:permission-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        
        # Se a resposta for paginada, verificar 'results'
        if 'results' in response_data:
            self.assertEqual(len(response_data['results']), 2)
        else:
            self.assertEqual(len(response_data), 2)
    
    def test_create_permission_as_admin(self):
        """Testa criação de permissão como admin"""
        self.authenticate_user(self.admin_user)
        
        url = reverse('users:permission-list')
        data = {
            'access_profile': self.access_profile.pk,
            'module': 'TASKS',
            'action': 'CREATE'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Permission.objects.filter(
                access_profile=self.access_profile,
                module='TASKS',
                action='CREATE'
            ).exists()
        )
    
    def test_list_permissions_without_permission(self):
        """Testa listagem de permissões sem permissão"""
        self.authenticate_user(self.regular_user)
        
        url = reverse('users:permission-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UnauthenticatedViewsTest(TestCase):
    """Testes para views não autenticadas"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_access_protected_endpoint_without_auth(self):
        """Testa acesso a endpoint protegido sem autenticação"""
        url = reverse('users:user-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
