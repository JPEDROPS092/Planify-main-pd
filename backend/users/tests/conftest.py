"""
Fixtures compartilhadas para os testes do módulo Users usando pytest.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta
from users.models import (
    UserProfile, AccessProfile, Permission, UserAccessProfile, 
    PasswordHistory, AuditLog, AccessAttempt, BlacklistedTokens
)

User = get_user_model()


@pytest.fixture
def api_client():
    """Cliente API para testes."""
    return APIClient()


@pytest.fixture
def admin_user():
    """Usuário administrador."""
    return User.objects.create_user(
        username='admin',
        email='admin@example.com',
        full_name='Admin User',
        password='adminpass123',
        role='ADMIN',
        is_staff=True,
        is_superuser=True,
        is_active=True
    )


@pytest.fixture
def project_manager_user():
    """Usuário gerente de projeto."""
    return User.objects.create_user(
        username='pm_user',
        email='pm@example.com',
        full_name='Project Manager',
        password='pmpass123',
        role='PROJECT_MANAGER',
        is_active=True
    )


@pytest.fixture
def team_leader_user():
    """Usuário líder de equipe."""
    return User.objects.create_user(
        username='tl_user',
        email='tl@example.com',
        full_name='Team Leader',
        password='tlpass123',
        role='TEAM_LEADER',
        is_active=True
    )


@pytest.fixture
def team_member_user():
    """Usuário membro da equipe."""
    return User.objects.create_user(
        username='tm_user',
        email='tm@example.com',
        full_name='Team Member',
        password='tmpass123',
        role='TEAM_MEMBER',
        is_active=True
    )


@pytest.fixture
def stakeholder_user():
    """Usuário stakeholder."""
    return User.objects.create_user(
        username='sh_user',
        email='stakeholder@example.com',
        full_name='Stakeholder User',
        password='shpass123',
        role='STAKEHOLDER',
        is_active=True
    )


@pytest.fixture
def inactive_user():
    """Usuário inativo."""
    return User.objects.create_user(
        username='inactive_user',
        email='inactive@example.com',
        full_name='Inactive User',
        password='inactivepass123',
        role='TEAM_MEMBER',
        is_active=False
    )


@pytest.fixture
def locked_user():
    """Usuário bloqueado por tentativas de login."""
    user = User.objects.create_user(
        username='locked_user',
        email='locked@example.com',
        full_name='Locked User',
        password='lockedpass123',
        role='TEAM_MEMBER',
        is_active=True,
        is_locked=True,
        failed_login_attempts=5
    )
    return user


@pytest.fixture
def authenticated_admin_client(api_client, admin_user):
    """Cliente API autenticado com usuário admin."""
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def authenticated_pm_client(api_client, project_manager_user):
    """Cliente API autenticado com usuário PM."""
    api_client.force_authenticate(user=project_manager_user)
    return api_client


@pytest.fixture
def authenticated_member_client(api_client, team_member_user):
    """Cliente API autenticado com usuário membro."""
    api_client.force_authenticate(user=team_member_user)
    return api_client


@pytest.fixture
def user_profile(team_member_user):
    """Perfil de usuário de teste."""
    return UserProfile.objects.create(
        user=team_member_user,
        phone='+5511999999999',
        theme_preference='DARK',
        email_notifications=True,
        system_notifications=False
    )


@pytest.fixture
def access_profile_admin():
    """Perfil de acesso de administrador."""
    return AccessProfile.objects.create(
        name='Admin Profile',
        description='Full access profile for administrators'
    )


@pytest.fixture
def access_profile_manager():
    """Perfil de acesso de gerente."""
    return AccessProfile.objects.create(
        name='Manager Profile',
        description='Management access profile'
    )


@pytest.fixture
def access_profile_member():
    """Perfil de acesso de membro."""
    return AccessProfile.objects.create(
        name='Member Profile',
        description='Basic member access profile'
    )


@pytest.fixture
def permission_view_projects(access_profile_member):
    """Permissão para visualizar projetos."""
    return Permission.objects.create(
        access_profile=access_profile_member,
        module='PROJECTS',
        action='VIEW'
    )


@pytest.fixture
def permission_create_tasks(access_profile_manager):
    """Permissão para criar tarefas."""
    return Permission.objects.create(
        access_profile=access_profile_manager,
        module='TASKS',
        action='CREATE'
    )


@pytest.fixture
def permission_edit_users(access_profile_admin):
    """Permissão para editar usuários."""
    return Permission.objects.create(
        access_profile=access_profile_admin,
        module='USERS',
        action='EDIT'
    )


@pytest.fixture
def user_access_profile(team_member_user, access_profile_member):
    """Relacionamento usuário-perfil de acesso."""
    return UserAccessProfile.objects.create(
        user=team_member_user,
        access_profile=access_profile_member
    )


@pytest.fixture
def password_history(team_member_user):
    """Histórico de senhas."""
    return PasswordHistory.objects.create(
        user=team_member_user,
        password_hash='old_password_hash_123'
    )


@pytest.fixture
def audit_log_login(team_member_user):
    """Log de auditoria de login."""
    return AuditLog.objects.create(
        user=team_member_user,
        action='LOGIN',
        ip_address='192.168.1.100',
        user_agent='Mozilla/5.0 Test Browser',
        details={'success': True}
    )


@pytest.fixture
def audit_log_failed_login(team_member_user):
    """Log de auditoria de login falhado."""
    return AuditLog.objects.create(
        user=team_member_user,
        action='FAILED_LOGIN',
        ip_address='192.168.1.100',
        user_agent='Mozilla/5.0 Test Browser',
        details={'reason': 'invalid_password'}
    )


@pytest.fixture
def access_attempt_success(team_member_user):
    """Tentativa de acesso bem-sucedida."""
    return AccessAttempt.objects.create(
        user=team_member_user,
        endpoint='/api/projects/',
        method='GET',
        ip_address='192.168.1.100',
        timestamp=timezone.now(),
        success=True
    )


@pytest.fixture
def access_attempt_failed(team_member_user):
    """Tentativa de acesso falhada."""
    return AccessAttempt.objects.create(
        user=team_member_user,
        endpoint='/api/admin/',
        method='GET',
        ip_address='192.168.1.100',
        timestamp=timezone.now(),
        success=False
    )


@pytest.fixture
def blacklisted_token(team_member_user):
    """Token na blacklist."""
    return BlacklistedTokens.objects.create(
        token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.test.token',
        user=team_member_user
    )


@pytest.fixture
def multiple_users(admin_user, project_manager_user, team_leader_user, team_member_user, stakeholder_user):
    """Fixture que retorna múltiplos usuários para testes."""
    return [admin_user, project_manager_user, team_leader_user, team_member_user, stakeholder_user]


@pytest.fixture
def user_with_complex_setup(team_member_user, user_profile, user_access_profile, password_history):
    """Usuário com configuração completa para testes de integração."""
    return team_member_user


# Aliases para compatibilidade com testes
@pytest.fixture 
def admin_access_profile():
    """Alias para access_profile_admin."""
    return AccessProfile.objects.create(
        name='Admin Access Profile',
        description='Full access profile for administrators'
    )


@pytest.fixture
def manager_access_profile():
    """Alias para access_profile_manager."""  
    return AccessProfile.objects.create(
        name='Manager Access Profile',
        description='Management access profile'
    )


@pytest.fixture
def user_data():
    """Dados básicos para criação de usuário."""
    return {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'full_name': 'Test User',
        'role': 'TEAM_MEMBER'
    }


@pytest.fixture
def user_profile_data():
    """Dados básicos para criação de perfil de usuário."""
    return {
        'phone': '+5511999999999',
        'theme_preference': 'LIGHT',
        'email_notifications': True,
        'system_notifications': True
    }


@pytest.fixture
def view_permission(access_profile_member):
    """Permissão de visualização para testes."""
    return Permission.objects.create(
        access_profile=access_profile_member,
        module='PROJECTS',
        action='VIEW'
    )


@pytest.fixture
def create_permission(access_profile_manager):
    """Permissão de criação para testes."""
    return Permission.objects.create(
        access_profile=access_profile_manager,
        module='PROJECTS',
        action='CREATE'
    )


@pytest.fixture
def edit_permission(access_profile_admin):
    """Permissão de edição para testes."""
    return Permission.objects.create(
        access_profile=access_profile_admin,
        module='USERS',
        action='EDIT'
    )


@pytest.fixture
def delete_permission(access_profile_admin):
    """Permissão de exclusão para testes."""
    return Permission.objects.create(
        access_profile=access_profile_admin,
        module='USERS',
        action='DELETE'
    )
