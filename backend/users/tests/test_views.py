"""
Testes para as views do módulo users.
Cobre UserViewSet, UserProfileViewSet e PermissionViewSet.
"""
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch, MagicMock

from users.models import UserProfile, AccessProfile, Permission, UserAccessProfile

User = get_user_model()


@pytest.mark.django_db
class TestUserViewSet:
    """Testes para UserViewSet"""
    
    def test_list_users_as_admin(self, api_client, admin_user, admin_access_profile):
        """Testa listagem de usuários como administrador"""
        # Atribuir perfil de acesso admin
        UserAccessProfile.objects.create(user=admin_user, access_profile=admin_access_profile)
        
        api_client.force_authenticate(user=admin_user)
        url = reverse('users:user-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
    
    def test_list_users_permission_denied(self, api_client, team_member_user):
        """Testa negação de acesso para listagem de usuários sem permissão"""
        api_client.force_authenticate(user=team_member_user)
        url = reverse('users:user-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_retrieve_user_as_admin(self, api_client, admin_user, team_member_user, admin_access_profile):
        """Testa obter detalhes de usuário como administrador"""
        # Atribuir perfil de acesso admin
        UserAccessProfile.objects.create(user=admin_user, access_profile=admin_access_profile)
        
        api_client.force_authenticate(user=admin_user)
        url = reverse('users:user-detail', kwargs={'pk': team_member_user.pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == team_member_user.username
        assert response.data['email'] == team_member_user.email
    
    def test_retrieve_user_not_found(self, api_client, admin_user, admin_access_profile):
        """Testa busca de usuário inexistente"""
        # Atribuir perfil de acesso admin
        UserAccessProfile.objects.create(user=admin_user, access_profile=admin_access_profile)
        
        api_client.force_authenticate(user=admin_user)
        url = reverse('users:user-detail', kwargs={'pk': 99999})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_create_user_as_admin(self, api_client, admin_user, admin_access_profile, user_data):
        """Testa criação de usuário como administrador"""
        # Atribuir perfil de acesso admin
        UserAccessProfile.objects.create(user=admin_user, access_profile=admin_access_profile)
        
        api_client.force_authenticate(user=admin_user)
        url = reverse('users:user-list')
        
        data = user_data.copy()
        data['password'] = 'TestPass123!'
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username=data['username']).exists()
    
    def test_create_user_permission_denied(self, api_client, team_member_user, user_data):
        """Testa negação de acesso para criação de usuário sem permissão"""
        api_client.force_authenticate(user=team_member_user)
        url = reverse('users:user-list')
        
        data = user_data.copy()
        data['password'] = 'TestPass123!'
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_create_user_invalid_data(self, api_client, admin_user, admin_access_profile):
        """Testa criação de usuário com dados inválidos"""
        # Atribuir perfil de acesso admin
        UserAccessProfile.objects.create(user=admin_user, access_profile=admin_access_profile)
        
        api_client.force_authenticate(user=admin_user)
        url = reverse('users:user-list')
        
        # Dados inválidos (email duplicado)
        data = {
            'username': 'newuser',
            'email': admin_user.email,  # Email já existe
            'full_name': 'New User',
            'password': 'TestPass123!'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data
    
    def test_update_user_as_admin(self, api_client, admin_user, team_member_user, admin_access_profile):
        """Testa atualização de usuário como administrador"""
        # Atribuir perfil de acesso admin
        UserAccessProfile.objects.create(user=admin_user, access_profile=admin_access_profile)
        
        api_client.force_authenticate(user=admin_user)
        url = reverse('users:user-detail', kwargs={'pk': team_member_user.pk})
        
        data = {
            'username': team_member_user.username,
            'email': team_member_user.email,
            'full_name': 'Updated Name',
            'role': 'TEAM_LEADER'
        }
        
        response = api_client.put(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        team_member_user.refresh_from_db()
        assert team_member_user.full_name == 'Updated Name'
        assert team_member_user.role == 'TEAM_LEADER'
    
    def test_partial_update_user(self, api_client, admin_user, team_member_user, admin_access_profile):
        """Testa atualização parcial de usuário"""
        # Atribuir perfil de acesso admin
        UserAccessProfile.objects.create(user=admin_user, access_profile=admin_access_profile)
        
        api_client.force_authenticate(user=admin_user)
        url = reverse('users:user-detail', kwargs={'pk': team_member_user.pk})
        
        data = {'full_name': 'Partially Updated Name'}
        
        response = api_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        team_member_user.refresh_from_db()
        assert team_member_user.full_name == 'Partially Updated Name'
    
    def test_delete_user_as_admin(self, api_client, admin_user, team_member_user, admin_access_profile):
        """Testa exclusão de usuário como administrador"""
        # Atribuir perfil de acesso admin
        UserAccessProfile.objects.create(user=admin_user, access_profile=admin_access_profile)
        
        api_client.force_authenticate(user=admin_user)
        url = reverse('users:user-detail', kwargs={'pk': team_member_user.pk})
        
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(pk=team_member_user.pk).exists()
    
    def test_me_action(self, api_client, team_member_user):
        """Testa ação 'me' - informações do usuário autenticado"""
        api_client.force_authenticate(user=team_member_user)
        url = reverse('users:user-me')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == team_member_user.username
        assert response.data['email'] == team_member_user.email
    
    def test_permissions_action(self, api_client, team_member_user, manager_access_profile):
        """Testa ação 'permissions' - permissões do usuário autenticado"""
        # Atribuir perfil de acesso
        UserAccessProfile.objects.create(user=team_member_user, access_profile=manager_access_profile)
        
        api_client.force_authenticate(user=team_member_user)
        url = reverse('users:user-permissions')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'role' in response.data
        assert 'permissions' in response.data
        assert response.data['role'] == team_member_user.role
    
    def test_change_password_action(self, api_client, team_member_user):
        """Testa ação 'change_password' - alterar senha"""
        api_client.force_authenticate(user=team_member_user)
        url = reverse('users:user-change-password')
        
        data = {
            'old_password': 'tmpass123',  # Senha correta do fixture
            'new_password': 'NewTestPass123!'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'detail' in response.data
        
        # Verificar se a senha foi alterada
        team_member_user.refresh_from_db()
        assert team_member_user.check_password('NewTestPass123!')
    
    def test_change_password_wrong_old_password(self, api_client, team_member_user):
        """Testa alteração de senha com senha atual incorreta"""
        api_client.force_authenticate(user=team_member_user)
        url = reverse('users:user-change-password')
        
        data = {
            'old_password': 'wrongpassword',
            'new_password': 'NewTestPass123!'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'old_password' in response.data
    
    @patch('users.views.send_mail')
    def test_reset_password_action(self, mock_send_mail, api_client, admin_user, team_member_user, admin_access_profile):
        """Testa ação 'reset_password' - redefinir senha"""
        # Atribuir perfil de acesso admin
        UserAccessProfile.objects.create(user=admin_user, access_profile=admin_access_profile)
        
        api_client.force_authenticate(user=admin_user)
        url = reverse('users:user-reset-password', kwargs={'pk': team_member_user.pk})
        
        response = api_client.post(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'detail' in response.data
        
        # Verificar se o email foi enviado
        mock_send_mail.assert_called_once()
        
        # Verificar se o perfil foi criado/atualizado
        team_member_user.refresh_from_db()
        profile = getattr(team_member_user, 'profile', None)
        if profile:
            assert profile.password_change_required
    
    def test_activate_user_action(self, api_client, admin_user, admin_access_profile):
        """Testa ação 'activate' - ativar usuário"""
        # Criar usuário inativo
        inactive_user = User(
            username='inactive',
            email='inactive@test.com',
            full_name='Inactive User',
            is_active=False
        )
        inactive_user.set_password('testpass123')
        inactive_user.save()
        
        # Atribuir perfil de acesso admin
        UserAccessProfile.objects.create(user=admin_user, access_profile=admin_access_profile)
        
        api_client.force_authenticate(user=admin_user)
        url = reverse('users:user-activate', kwargs={'pk': inactive_user.pk})
        
        response = api_client.post(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'detail' in response.data
        
        inactive_user.refresh_from_db()
        assert inactive_user.is_active
    
    def test_deactivate_user_action(self, api_client, admin_user, team_member_user, admin_access_profile):
        """Testa ação 'deactivate' - desativar usuário"""
        # Atribuir perfil de acesso admin
        UserAccessProfile.objects.create(user=admin_user, access_profile=admin_access_profile)
        
        api_client.force_authenticate(user=admin_user)
        url = reverse('users:user-deactivate', kwargs={'pk': team_member_user.pk})
        
        response = api_client.post(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'detail' in response.data
        
        team_member_user.refresh_from_db()
        assert not team_member_user.is_active
    
    def test_unlock_user_action(self, api_client, admin_user, admin_access_profile):
        """Testa ação 'unlock' - desbloquear usuário"""
        # Criar usuário bloqueado
        locked_user = User(
            username='locked',
            email='locked@test.com',
            full_name='Locked User',
            is_locked=True,
            failed_login_attempts=5
        )
        locked_user.set_password('testpass123')
        locked_user.save()
        
        # Atribuir perfil de acesso admin
        UserAccessProfile.objects.create(user=admin_user, access_profile=admin_access_profile)
        
        api_client.force_authenticate(user=admin_user)
        url = reverse('users:user-unlock', kwargs={'pk': locked_user.pk})
        
        response = api_client.post(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'detail' in response.data
        
        locked_user.refresh_from_db()
        assert not locked_user.is_locked
        assert locked_user.failed_login_attempts == 0


@pytest.mark.django_db
class TestUserProfileViewSet:
    """Testes para UserProfileViewSet"""
    
    def test_list_profiles(self, api_client, team_member_user, user_profile):
        """Testa listagem de perfis"""
        api_client.force_authenticate(user=team_member_user)
        url = reverse('users:profile-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
    
    def test_retrieve_profile(self, api_client, team_member_user, user_profile):
        """Testa obter detalhes de perfil"""
        api_client.force_authenticate(user=team_member_user)
        url = reverse('users:profile-detail', kwargs={'pk': user_profile.pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['theme_preference'] == user_profile.theme_preference
    
    def test_create_profile(self, api_client, team_member_user):
        """Testa criação de perfil"""
        # Criar usuário sem perfil
        user_without_profile = User(
            username='noprofile',
            email='noprofile@test.com',
            full_name='No Profile User'
        )
        user_without_profile.set_password('testpass123')
        user_without_profile.save()
        
        api_client.force_authenticate(user=team_member_user)
        url = reverse('users:profile-list')
        
        data = {
            'user': user_without_profile.pk,
            'phone': '+55 11 99999-9999',
            'theme_preference': 'LIGHT',
            'email_notifications': True,
            'system_notifications': True
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert UserProfile.objects.filter(user=user_without_profile).exists()
    
    def test_update_profile(self, api_client, team_member_user, user_profile):
        """Testa atualização de perfil"""
        api_client.force_authenticate(user=team_member_user)
        url = reverse('users:profile-detail', kwargs={'pk': user_profile.pk})
        
        data = {
            'phone': '+55 11 99999-9999',
            'theme_preference': 'DARK',
            'email_notifications': False,
            'system_notifications': True
        }
        
        response = api_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        user_profile.refresh_from_db()
        assert user_profile.phone == '+55 11 99999-9999'
        assert user_profile.theme_preference == 'DARK'
        assert not user_profile.email_notifications
    
    def test_delete_profile(self, api_client, team_member_user, user_profile):
        """Testa exclusão de perfil"""
        api_client.force_authenticate(user=team_member_user)
        url = reverse('users:profile-detail', kwargs={'pk': user_profile.pk})
        
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not UserProfile.objects.filter(pk=user_profile.pk).exists()


@pytest.mark.django_db
class TestPermissionViewSet:
    """Testes para PermissionViewSet"""
    
    def test_list_permissions_as_admin(self, api_client, admin_user, admin_access_profile, view_permission):
        """Testa listagem de permissões como administrador"""
        # Atribuir perfil de acesso admin
        UserAccessProfile.objects.create(user=admin_user, access_profile=admin_access_profile)
        
        api_client.force_authenticate(user=admin_user)
        url = reverse('users:permission-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
    
    def test_list_permissions_permission_denied(self, api_client, team_member_user):
        """Testa negação de acesso para listagem de permissões"""
        api_client.force_authenticate(user=team_member_user)
        url = reverse('users:permission-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_retrieve_permission(self, api_client, admin_user, admin_access_profile, view_permission):
        """Testa obter detalhes de permissão"""
        # Atribuir perfil de acesso admin
        UserAccessProfile.objects.create(user=admin_user, access_profile=admin_access_profile)
        
        api_client.force_authenticate(user=admin_user)
        url = reverse('users:permission-detail', kwargs={'pk': view_permission.pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['module'] == view_permission.module
        assert response.data['action'] == view_permission.action
    
    def test_create_permission(self, api_client, admin_user, admin_access_profile, manager_access_profile):
        """Testa criação de permissão"""
        # Atribuir perfil de acesso admin
        UserAccessProfile.objects.create(user=admin_user, access_profile=admin_access_profile)
        
        api_client.force_authenticate(user=admin_user)
        url = reverse('users:permission-list')
        
        data = {
            'access_profile': manager_access_profile.pk,
            'module': 'TASKS',
            'action': 'CREATE'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Permission.objects.filter(
            access_profile=manager_access_profile,
            module='TASKS',
            action='CREATE'
        ).exists()
    
    def test_create_permission_duplicate(self, api_client, admin_user, admin_access_profile, view_permission):
        """Testa criação de permissão duplicada"""
        # Atribuir perfil de acesso admin
        UserAccessProfile.objects.create(user=admin_user, access_profile=admin_access_profile)
        
        api_client.force_authenticate(user=admin_user)
        url = reverse('users:permission-list')
        
        data = {
            'access_profile': view_permission.access_profile.pk,
            'module': view_permission.module,
            'action': view_permission.action
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_filter_permissions(self, api_client, admin_user, admin_access_profile, view_permission, create_permission):
        """Testa filtros de permissões"""
        # Atribuir perfil de acesso admin
        UserAccessProfile.objects.create(user=admin_user, access_profile=admin_access_profile)
        
        api_client.force_authenticate(user=admin_user)
        
        # Filtrar por módulo
        url = reverse('users:permission-list')
        response = api_client.get(url, {'module': 'PROJECTS'})
        
        assert response.status_code == status.HTTP_200_OK
        
        # Filtrar por ação
        response = api_client.get(url, {'action': 'VIEW'})
        
        assert response.status_code == status.HTTP_200_OK
        
        # Filtrar por perfil de acesso
        response = api_client.get(url, {'access_profile': view_permission.access_profile.pk})
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_update_permission(self, api_client, admin_user, admin_access_profile, view_permission):
        """Testa atualização de permissão"""
        # Atribuir perfil de acesso admin
        UserAccessProfile.objects.create(user=admin_user, access_profile=admin_access_profile)
        
        api_client.force_authenticate(user=admin_user)
        url = reverse('users:permission-detail', kwargs={'pk': view_permission.pk})
        
        data = {
            'access_profile': view_permission.access_profile.pk,
            'module': 'TASKS',
            'action': 'EDIT'
        }
        
        response = api_client.put(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        view_permission.refresh_from_db()
        assert view_permission.module == 'TASKS'
        assert view_permission.action == 'EDIT'
    
    def test_delete_permission(self, api_client, admin_user, admin_access_profile, view_permission):
        """Testa exclusão de permissão"""
        # Atribuir perfil de acesso admin
        UserAccessProfile.objects.create(user=admin_user, access_profile=admin_access_profile)
        
        api_client.force_authenticate(user=admin_user)
        url = reverse('users:permission-detail', kwargs={'pk': view_permission.pk})
        
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Permission.objects.filter(pk=view_permission.pk).exists()


@pytest.mark.django_db
class TestAuthenticationViews:
    """Testes para views de autenticação"""
    
    def test_unauthenticated_access(self, api_client):
        """Testa acesso não autenticado a endpoints protegidos"""
        endpoints = [
            reverse('users:user-list'),
            reverse('users:user-me'),
            reverse('users:permission-list'),
        ]
        
        for endpoint in endpoints:
            response = api_client.get(endpoint)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_authenticated_access_no_permission(self, api_client, team_member_user):
        """Testa acesso autenticado sem permissão adequada"""
        api_client.force_authenticate(user=team_member_user)
        
        # Endpoints que requerem permissões específicas
        protected_endpoints = [
            reverse('users:user-list'),
            reverse('users:permission-list'),
        ]
        
        for endpoint in protected_endpoints:
            response = api_client.get(endpoint)
            assert response.status_code == status.HTTP_403_FORBIDDEN
