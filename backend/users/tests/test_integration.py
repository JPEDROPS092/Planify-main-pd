"""
Testes de integração para o módulo users.
Cobre fluxos completos de usuário, autenticação, permissões e segurança.
"""
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch, MagicMock
from django.utils import timezone
from datetime import timedelta

from users.models import (
    UserProfile, AccessProfile, Permission, UserAccessProfile,
    PasswordHistory, AccessAttempt, AuditLog, BlacklistedTokens
)

User = get_user_model()


@pytest.mark.django_db
class TestUserCompleteFlow:
    """Testes de fluxo completo de usuário"""
    
    def test_user_creation_to_operation_flow(self, api_client, admin_user, admin_access_profile):
        """Testa fluxo completo: Criação → Ativação → Login → Operações → Logout"""
        # 1. Admin cria usuário
        UserAccessProfile.objects.create(user=admin_user, access_profile=admin_access_profile)
        api_client.force_authenticate(user=admin_user)
        
        user_data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'full_name': 'New User',
            'password': 'TestPass123!',
            'role': 'TEAM_MEMBER'
        }
        
        url = reverse('users:user-list')
        response = api_client.post(url, user_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        new_user = User.objects.get(username='newuser')
        
        # 2. Verificar se usuário foi criado com perfil
        assert hasattr(new_user, 'profile')
        assert new_user.is_active
        
        # 3. Usuário acessa suas próprias informações
        api_client.force_authenticate(user=new_user)
        me_url = reverse('users:user-me')
        response = api_client.get(me_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'newuser'
        
        # 4. Usuário altera sua senha
        change_password_url = reverse('users:user-change-password')
        password_data = {
            'old_password': 'TestPass123!',
            'new_password': 'NewTestPass456!'
        }
        
        response = api_client.post(change_password_url, password_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        
        # 5. Verificar alteração de senha
        new_user.refresh_from_db()
        assert new_user.check_password('NewTestPass456!')
    
    def test_user_with_profile_creation(self, api_client, admin_user, admin_access_profile):
        """Testa criação de usuário com perfil personalizado"""
        UserAccessProfile.objects.create(user=admin_user, access_profile=admin_access_profile)
        api_client.force_authenticate(user=admin_user)
        
        user_data = {
            'username': 'profileuser',
            'email': 'profileuser@test.com',
            'full_name': 'Profile User',
            'password': 'TestPass123!',
            'profile': {
                'phone': '+55 11 99999-9999',
                'theme_preference': 'DARK',
                'email_notifications': False
            }
        }
        
        url = reverse('users:user-list')
        response = api_client.post(url, user_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        
        new_user = User.objects.get(username='profileuser')
        profile = new_user.profile
        
        assert profile.phone == '+55 11 99999-9999'
        assert profile.theme_preference == 'DARK'
        assert not profile.email_notifications


@pytest.mark.django_db
class TestPermissionFlow:
    """Testes de fluxo de permissões"""
    
    def test_access_profile_assignment_flow(self, api_client, admin_user, team_member_user):
        """Testa fluxo completo de atribuição de perfis de acesso"""
        # 1. Criar perfil de acesso
        access_profile = AccessProfile.objects.create(
            name='Editor Profile',
            description='Can edit projects and tasks'
        )
        
        # 2. Criar permissões para o perfil
        permissions_data = [
            ('PROJECTS', 'VIEW'),
            ('PROJECTS', 'EDIT'),
            ('TASKS', 'VIEW'),
            ('TASKS', 'CREATE'),
            ('TASKS', 'EDIT')
        ]
        
        for module, action in permissions_data:
            Permission.objects.create(
                access_profile=access_profile,
                module=module,
                action=action
            )
        
        # 3. Atribuir perfil ao usuário
        UserAccessProfile.objects.create(
            user=team_member_user,
            access_profile=access_profile
        )
        
        # 4. Verificar permissões do usuário
        api_client.force_authenticate(user=team_member_user)
        permissions_url = reverse('users:user-permissions')
        response = api_client.get(permissions_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'permissions' in response.data
        
        expected_permissions = [f"{module}.{action}" for module, action in permissions_data]
        for perm in expected_permissions:
            assert perm in response.data['permissions']
    
    def test_multiple_access_profiles(self, api_client, team_member_user):
        """Testa usuário com múltiplos perfis de acesso"""
        # Criar dois perfis diferentes
        profile1 = AccessProfile.objects.create(
            name='Projects Manager',
            description='Manages projects'
        )
        
        profile2 = AccessProfile.objects.create(
            name='Tasks Editor',
            description='Edits tasks'
        )
        
        # Adicionar permissões diferentes para cada perfil
        Permission.objects.create(access_profile=profile1, module='PROJECTS', action='VIEW')
        Permission.objects.create(access_profile=profile1, module='PROJECTS', action='EDIT')
        Permission.objects.create(access_profile=profile2, module='TASKS', action='VIEW')
        Permission.objects.create(access_profile=profile2, module='TASKS', action='EDIT')
        
        # Atribuir ambos os perfis ao usuário
        UserAccessProfile.objects.create(user=team_member_user, access_profile=profile1)
        UserAccessProfile.objects.create(user=team_member_user, access_profile=profile2)
        
        # Verificar permissões combinadas
        api_client.force_authenticate(user=team_member_user)
        permissions_url = reverse('users:user-permissions')
        response = api_client.get(permissions_url)
        
        assert response.status_code == status.HTTP_200_OK
        permissions = response.data['permissions']
        
        expected_permissions = [
            'PROJECTS.VIEW', 'PROJECTS.EDIT',
            'TASKS.VIEW', 'TASKS.EDIT'
        ]
        
        for perm in expected_permissions:
            assert perm in permissions


@pytest.mark.django_db
class TestSecurityFlow:
    """Testes de fluxo de segurança"""
    
    def test_password_history_flow(self, api_client, team_member_user):
        """Testa fluxo de histórico de senhas"""
        initial_password = 'TestPass123!'
        team_member_user.set_password(initial_password)
        team_member_user.save()
        
        api_client.force_authenticate(user=team_member_user)
        change_password_url = reverse('users:user-change-password')
        
        # Alterar senha múltiplas vezes
        passwords = ['NewPass123!', 'AnotherPass456!', 'FinalPass789!']
        
        previous_password = initial_password
        for new_password in passwords:
            password_data = {
                'old_password': previous_password,
                'new_password': new_password
            }
            
            response = api_client.post(change_password_url, password_data, format='json')
            assert response.status_code == status.HTTP_200_OK
            
            # Verificar se histórico foi criado
            assert PasswordHistory.objects.filter(user=team_member_user).exists()
            
            previous_password = new_password
        
        # Verificar limite de histórico (máximo 5)
        history_count = PasswordHistory.objects.filter(user=team_member_user).count()
        assert history_count <= 5
    
    def test_account_locking_flow(self, api_client, team_member_user):
        """Testa fluxo de bloqueio de conta por tentativas falhadas"""
        # Simular tentativas de login falhadas
        for i in range(5):
            team_member_user.increment_failed_login()
        
        team_member_user.refresh_from_db()
        assert team_member_user.is_locked
        assert team_member_user.failed_login_attempts == 5
        
        # Admin desbloqueia a conta
        admin_user = User(
            username='admin',
            email='admin@test.com',
            full_name='Admin User',
            role='ADMIN',
            is_superuser=True
        )
        admin_user.set_password('adminpass')
        admin_user.save()
        
        # Criar perfil de acesso admin
        admin_access_profile = AccessProfile.objects.create(name='Admin Access')
        Permission.objects.create(access_profile=admin_access_profile, module='USERS', action='EDIT')
        UserAccessProfile.objects.create(user=admin_user, access_profile=admin_access_profile)
        
        api_client.force_authenticate(user=admin_user)
        unlock_url = reverse('users:user-unlock', kwargs={'pk': team_member_user.pk})
        response = api_client.post(unlock_url)
        
        assert response.status_code == status.HTTP_200_OK
        
        team_member_user.refresh_from_db()
        assert not team_member_user.is_locked
        assert team_member_user.failed_login_attempts == 0
    
    @patch('users.views.send_mail')
    def test_password_reset_flow(self, mock_send_mail, api_client, admin_user, team_member_user):
        """Testa fluxo completo de reset de senha"""
        # Criar perfil de acesso admin
        admin_access_profile = AccessProfile.objects.create(name='Admin Access')
        Permission.objects.create(access_profile=admin_access_profile, module='USERS', action='EDIT')
        UserAccessProfile.objects.create(user=admin_user, access_profile=admin_access_profile)
        
        # Admin faz reset da senha do usuário
        api_client.force_authenticate(user=admin_user)
        reset_url = reverse('users:user-reset-password', kwargs={'pk': team_member_user.pk})
        response = api_client.post(reset_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert mock_send_mail.called
        
        # Verificar se perfil foi atualizado para exigir mudança de senha
        team_member_user.refresh_from_db()
        if hasattr(team_member_user, 'profile'):
            assert team_member_user.profile.password_change_required


@pytest.mark.django_db
class TestAuditFlow:
    """Testes de fluxo de auditoria"""
    
    def test_audit_log_creation(self, team_member_user):
        """Testa criação de logs de auditoria"""
        # Criar log de auditoria
        audit_log = AuditLog.objects.create(
            user=team_member_user,
            action='LOGIN',
            ip_address='192.168.1.1',
            user_agent='Test Browser',
            details={'success': True}
        )
        
        assert audit_log.user == team_member_user
        assert audit_log.action == 'LOGIN'
        assert audit_log.ip_address == '192.168.1.1'
        assert audit_log.details['success'] is True
    
    def test_access_attempt_logging(self, team_member_user):
        """Testa registro de tentativas de acesso"""
        access_attempt = AccessAttempt.objects.create(
            user=team_member_user,
            endpoint='/api/users/me/',
            method='GET',
            ip_address='192.168.1.1',
            timestamp=timezone.now(),
            success=True
        )
        
        assert access_attempt.user == team_member_user
        assert access_attempt.endpoint == '/api/users/me/'
        assert access_attempt.success is True


@pytest.mark.django_db
class TestTokenManagement:
    """Testes de gerenciamento de tokens"""
    
    def test_blacklist_token_flow(self, team_member_user):
        """Testa fluxo de blacklist de tokens"""
        # Criar token blacklisted
        token = BlacklistedTokens.objects.create(
            token='fake_token_string',
            user=team_member_user
        )
        
        assert token.user == team_member_user
        assert token.token == 'fake_token_string'
        assert token.created_at is not None


@pytest.mark.django_db
class TestDataIntegrity:
    """Testes de integridade de dados"""
    
    def test_user_deletion_cascade(self, team_member_user):
        """Testa deleção em cascata quando usuário é removido"""
        # Criar dados relacionados
        profile = UserProfile.objects.create(
            user=team_member_user,
            phone='+55 11 99999-9999'
        )
        
        audit_log = AuditLog.objects.create(
            user=team_member_user,
            action='LOGIN'
        )
        
        password_history = PasswordHistory.objects.create(
            user=team_member_user,
            password_hash='old_hash'
        )
        
        access_attempt = AccessAttempt.objects.create(
            user=team_member_user,
            endpoint='/test/',
            method='GET',
            ip_address='127.0.0.1',
            timestamp=timezone.now()
        )
        
        blacklisted_token = BlacklistedTokens.objects.create(
            token='test_token',
            user=team_member_user
        )
        
        user_id = team_member_user.id
        
        # Deletar usuário
        team_member_user.delete()
        
        # Verificar se dados relacionados foram removidos
        assert not UserProfile.objects.filter(user_id=user_id).exists()
        assert not AuditLog.objects.filter(user_id=user_id).exists()
        assert not PasswordHistory.objects.filter(user_id=user_id).exists()
        assert not AccessAttempt.objects.filter(user_id=user_id).exists()
        assert not BlacklistedTokens.objects.filter(user_id=user_id).exists()
    
    def test_access_profile_deletion_cascade(self):
        """Testa deleção em cascata quando perfil de acesso é removido"""
        access_profile = AccessProfile.objects.create(
            name='Test Profile',
            description='Test Description'
        )
        
        # Criar permissões
        permission1 = Permission.objects.create(
            access_profile=access_profile,
            module='PROJECTS',
            action='VIEW'
        )
        
        permission2 = Permission.objects.create(
            access_profile=access_profile,
            module='TASKS',
            action='EDIT'
        )
        
        # Criar usuário e associação
        user = User(
            username='testuser',
            email='test@test.com',
            full_name='Test User'
        )
        user.set_password('testpass')
        user.save()
        
        user_access_profile = UserAccessProfile.objects.create(
            user=user,
            access_profile=access_profile
        )
        
        profile_id = access_profile.id
        
        # Deletar perfil de acesso
        access_profile.delete()
        
        # Verificar se dados relacionados foram removidos
        assert not Permission.objects.filter(access_profile_id=profile_id).exists()
        assert not UserAccessProfile.objects.filter(access_profile_id=profile_id).exists()


@pytest.mark.django_db
class TestEdgeCases:
    """Testes de casos extremos e validações"""
    
    def test_unique_constraints(self, user_data):
        """Testa constraints de unicidade"""
        # Criar primeiro usuário
        user1 = User(
            username=user_data['username'],
            email=user_data['email'],
            full_name=user_data['full_name']
        )
        user1.set_password('testpass')
        user1.save()
        
        # Tentar criar usuário com mesmo username
        user2 = User(
            username=user_data['username'],  # Username duplicado
            email='different@test.com',
            full_name='Different User'
        )
        
        with pytest.raises(Exception):  # IntegrityError ou similar
            user2.save()
        
        # Tentar criar usuário com mesmo email
        user3 = User(
            username='differentuser',
            email=user_data['email'],  # Email duplicado
            full_name='Different User'
        )
        
        with pytest.raises(Exception):  # IntegrityError ou similar
            user3.save()
    
    def test_permission_unique_constraint(self):
        """Testa constraint de unicidade em Permission"""
        access_profile = AccessProfile.objects.create(
            name='Test Profile'
        )
        
        # Criar primeira permissão
        Permission.objects.create(
            access_profile=access_profile,
            module='PROJECTS',
            action='VIEW'
        )
        
        # Tentar criar permissão duplicada
        with pytest.raises(Exception):  # IntegrityError
            Permission.objects.create(
                access_profile=access_profile,
                module='PROJECTS',
                action='VIEW'
            )
    
    def test_user_access_profile_unique_constraint(self):
        """Testa constraint de unicidade em UserAccessProfile"""
        user = User(
            username='testuser',
            email='test@test.com',
            full_name='Test User'
        )
        user.set_password('testpass')
        user.save()
        
        access_profile = AccessProfile.objects.create(
            name='Test Profile'
        )
        
        # Criar primeira associação
        UserAccessProfile.objects.create(
            user=user,
            access_profile=access_profile
        )
        
        # Tentar criar associação duplicada
        with pytest.raises(Exception):  # IntegrityError
            UserAccessProfile.objects.create(
                user=user,
                access_profile=access_profile
            )
