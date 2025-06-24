"""
Testes para as fixtures do módulo users.
Verifica se todas as fixtures estão funcionando corretamente.
"""
import pytest
from django.contrib.auth import get_user_model
from users.models import (
    UserProfile, AccessProfile, Permission, UserAccessProfile,
    PasswordHistory, AuditLog, AccessAttempt, BlacklistedTokens
)

User = get_user_model()


@pytest.mark.django_db
class TestUserFixtures:
    """Testes para fixtures de usuários"""
    
    def test_admin_user_fixture(self, admin_user):
        """Testa fixture de usuário administrador"""
        assert admin_user.username == 'admin'
        assert admin_user.email == 'admin@example.com'
        assert admin_user.role == 'ADMIN'
        assert admin_user.is_staff is True
        assert admin_user.is_superuser is True
        assert admin_user.is_active is True
        assert admin_user.check_password('adminpass123')
    
    def test_project_manager_user_fixture(self, project_manager_user):
        """Testa fixture de usuário gerente de projeto"""
        assert project_manager_user.username == 'pm_user'
        assert project_manager_user.email == 'pm@example.com'
        assert project_manager_user.role == 'PROJECT_MANAGER'
        assert project_manager_user.is_active is True
        assert project_manager_user.check_password('pmpass123')
    
    def test_team_leader_user_fixture(self, team_leader_user):
        """Testa fixture de usuário líder de equipe"""
        assert team_leader_user.username == 'tl_user'
        assert team_leader_user.email == 'tl@example.com'
        assert team_leader_user.role == 'TEAM_LEADER'
        assert team_leader_user.is_active is True
        assert team_leader_user.check_password('tlpass123')
    
    def test_team_member_user_fixture(self, team_member_user):
        """Testa fixture de usuário membro da equipe"""
        assert team_member_user.username == 'tm_user'
        assert team_member_user.email == 'tm@example.com'
        assert team_member_user.role == 'TEAM_MEMBER'
        assert team_member_user.is_active is True
        assert team_member_user.check_password('tmpass123')
    
    def test_stakeholder_user_fixture(self, stakeholder_user):
        """Testa fixture de usuário stakeholder"""
        assert stakeholder_user.username == 'sh_user'
        assert stakeholder_user.email == 'stakeholder@example.com'
        assert stakeholder_user.role == 'STAKEHOLDER'
        assert stakeholder_user.is_active is True
        assert stakeholder_user.check_password('shpass123')
    
    def test_inactive_user_fixture(self, inactive_user):
        """Testa fixture de usuário inativo"""
        assert inactive_user.username == 'inactive_user'
        assert inactive_user.email == 'inactive@example.com'
        assert inactive_user.role == 'TEAM_MEMBER'
        assert inactive_user.is_active is False
        assert inactive_user.check_password('inactivepass123')
    
    def test_locked_user_fixture(self, locked_user):
        """Testa fixture de usuário bloqueado"""
        assert locked_user.username == 'locked_user'
        assert locked_user.email == 'locked@example.com'
        assert locked_user.is_locked is True
        assert locked_user.failed_login_attempts == 5
        assert locked_user.check_password('lockedpass123')


@pytest.mark.django_db
class TestAuthenticatedClientFixtures:
    """Testes para fixtures de clientes autenticados"""
    
    def test_authenticated_admin_client(self, authenticated_admin_client, admin_user):
        """Testa fixture de cliente admin autenticado"""
        # Verificar se o cliente está autenticado
        response = authenticated_admin_client.get('/api/users/me/')
        # Note: pode retornar 404 se a URL não existir, mas não deve ser 401
        assert response.status_code != 401  # Não deve ser não autorizado
    
    def test_authenticated_pm_client(self, authenticated_pm_client, project_manager_user):
        """Testa fixture de cliente PM autenticado"""
        response = authenticated_pm_client.get('/api/users/me/')
        assert response.status_code != 401
    
    def test_authenticated_member_client(self, authenticated_member_client, team_member_user):
        """Testa fixture de cliente membro autenticado"""
        response = authenticated_member_client.get('/api/users/me/')
        assert response.status_code != 401


@pytest.mark.django_db
class TestProfileFixtures:
    """Testes para fixtures de perfis"""
    
    def test_user_profile_fixture(self, user_profile, team_member_user):
        """Testa fixture de perfil de usuário"""
        assert user_profile.user == team_member_user
        assert user_profile.phone == '+5511999999999'
        assert user_profile.theme_preference == 'DARK'
        assert user_profile.email_notifications is True
        assert user_profile.system_notifications is False
    
    def test_access_profile_admin_fixture(self, access_profile_admin):
        """Testa fixture de perfil de acesso admin"""
        assert access_profile_admin.name == 'Admin Profile'
        assert 'administrators' in access_profile_admin.description
    
    def test_access_profile_manager_fixture(self, access_profile_manager):
        """Testa fixture de perfil de acesso manager"""
        assert access_profile_manager.name == 'Manager Profile'
        assert 'Management' in access_profile_manager.description
    
    def test_access_profile_member_fixture(self, access_profile_member):
        """Testa fixture de perfil de acesso member"""
        assert access_profile_member.name == 'Member Profile'
        assert 'member' in access_profile_member.description


@pytest.mark.django_db
class TestPermissionFixtures:
    """Testes para fixtures de permissões"""
    
    def test_permission_view_projects_fixture(self, permission_view_projects, access_profile_member):
        """Testa fixture de permissão de visualizar projetos"""
        assert permission_view_projects.access_profile == access_profile_member
        assert permission_view_projects.module == 'PROJECTS'
        assert permission_view_projects.action == 'VIEW'
    
    def test_permission_create_tasks_fixture(self, permission_create_tasks, access_profile_manager):
        """Testa fixture de permissão de criar tarefas"""
        assert permission_create_tasks.access_profile == access_profile_manager
        assert permission_create_tasks.module == 'TASKS'
        assert permission_create_tasks.action == 'CREATE'
    
    def test_permission_edit_users_fixture(self, permission_edit_users, access_profile_admin):
        """Testa fixture de permissão de editar usuários"""
        assert permission_edit_users.access_profile == access_profile_admin
        assert permission_edit_users.module == 'USERS'
        assert permission_edit_users.action == 'EDIT'
    
    def test_view_permission_fixture(self, view_permission, access_profile_member):
        """Testa fixture view_permission"""
        assert view_permission.access_profile == access_profile_member
        assert view_permission.module == 'PROJECTS'
        assert view_permission.action == 'VIEW'
    
    def test_create_permission_fixture(self, create_permission, access_profile_manager):
        """Testa fixture create_permission"""
        assert create_permission.access_profile == access_profile_manager
        assert create_permission.module == 'PROJECTS'
        assert create_permission.action == 'CREATE'
    
    def test_edit_permission_fixture(self, edit_permission, access_profile_admin):
        """Testa fixture edit_permission"""
        assert edit_permission.access_profile == access_profile_admin
        assert edit_permission.module == 'USERS'
        assert edit_permission.action == 'EDIT'
    
    def test_delete_permission_fixture(self, delete_permission, access_profile_admin):
        """Testa fixture delete_permission"""
        assert delete_permission.access_profile == access_profile_admin
        assert delete_permission.module == 'USERS'
        assert delete_permission.action == 'DELETE'


@pytest.mark.django_db
class TestUserAccessProfileFixtures:
    """Testes para fixtures de associação usuário-perfil"""
    
    def test_user_access_profile_fixture(self, user_access_profile, team_member_user, access_profile_member):
        """Testa fixture de associação usuário-perfil"""
        assert user_access_profile.user == team_member_user
        assert user_access_profile.access_profile == access_profile_member


@pytest.mark.django_db
class TestAuditFixtures:
    """Testes para fixtures de auditoria"""
    
    def test_password_history_fixture(self, password_history, team_member_user):
        """Testa fixture de histórico de senhas"""
        assert password_history.user == team_member_user
        assert password_history.password_hash == 'old_password_hash_123'
    
    def test_audit_log_login_fixture(self, audit_log_login, team_member_user):
        """Testa fixture de log de login"""
        assert audit_log_login.user == team_member_user
        assert audit_log_login.action == 'LOGIN'
        assert audit_log_login.ip_address == '192.168.1.100'
        assert audit_log_login.details['success'] is True
    
    def test_audit_log_failed_login_fixture(self, audit_log_failed_login, team_member_user):
        """Testa fixture de log de login falhado"""
        assert audit_log_failed_login.user == team_member_user
        assert audit_log_failed_login.action == 'FAILED_LOGIN'
        assert audit_log_failed_login.ip_address == '192.168.1.100'
        assert audit_log_failed_login.details['reason'] == 'invalid_password'
    
    def test_access_attempt_success_fixture(self, access_attempt_success, team_member_user):
        """Testa fixture de tentativa de acesso bem-sucedida"""
        assert access_attempt_success.user == team_member_user
        assert access_attempt_success.endpoint == '/api/projects/'
        assert access_attempt_success.method == 'GET'
        assert access_attempt_success.success is True
    
    def test_access_attempt_failed_fixture(self, access_attempt_failed, team_member_user):
        """Testa fixture de tentativa de acesso falhada"""
        assert access_attempt_failed.user == team_member_user
        assert access_attempt_failed.endpoint == '/api/admin/'
        assert access_attempt_failed.method == 'GET'
        assert access_attempt_failed.success is False
    
    def test_blacklisted_token_fixture(self, blacklisted_token, team_member_user):
        """Testa fixture de token blacklisted"""
        assert blacklisted_token.user == team_member_user
        assert blacklisted_token.token == 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.test.token'


@pytest.mark.django_db
class TestDataFixtures:
    """Testes para fixtures de dados"""
    
    def test_user_data_fixture(self, user_data):
        """Testa fixture de dados de usuário"""
        assert user_data['username'] == 'testuser'
        assert user_data['email'] == 'testuser@example.com'
        assert user_data['full_name'] == 'Test User'
        assert user_data['role'] == 'TEAM_MEMBER'
    
    def test_user_profile_data_fixture(self, user_profile_data):
        """Testa fixture de dados de perfil"""
        assert user_profile_data['phone'] == '+5511999999999'
        assert user_profile_data['theme_preference'] == 'LIGHT'
        assert user_profile_data['email_notifications'] is True
        assert user_profile_data['system_notifications'] is True


@pytest.mark.django_db
class TestMultipleFixtures:
    """Testes para fixtures compostas"""
    
    def test_multiple_users_fixture(self, multiple_users):
        """Testa fixture de múltiplos usuários"""
        assert len(multiple_users) == 5
        
        # Verificar se todos os usuários estão presentes
        usernames = [user.username for user in multiple_users]
        expected_usernames = ['admin', 'pm_user', 'tl_user', 'tm_user', 'sh_user']
        
        for username in expected_usernames:
            assert username in usernames
    
    def test_user_with_complex_setup_fixture(self, user_with_complex_setup, team_member_user):
        """Testa fixture de usuário com configuração complexa"""
        assert user_with_complex_setup == team_member_user
        
        # Verificar se tem perfil
        assert hasattr(user_with_complex_setup, 'profile')
        
        # Verificar se tem perfis de acesso
        assert user_with_complex_setup.access_profiles.exists()
        
        # Verificar se tem histórico de senhas
        assert user_with_complex_setup.password_history.exists()


@pytest.mark.django_db
class TestAliasFixtures:
    """Testes para fixtures alias"""
    
    def test_admin_access_profile_fixture(self, admin_access_profile):
        """Testa fixture alias admin_access_profile"""
        assert admin_access_profile.name == 'Admin Access Profile'
        assert 'administrators' in admin_access_profile.description
    
    def test_manager_access_profile_fixture(self, manager_access_profile):
        """Testa fixture alias manager_access_profile"""
        assert manager_access_profile.name == 'Manager Access Profile'
        assert 'Management' in manager_access_profile.description


@pytest.mark.django_db
class TestFixtureIntegration:
    """Testes de integração entre fixtures"""
    
    def test_user_profile_relationship(self, user_profile, team_member_user):
        """Testa relacionamento entre usuário e perfil"""
        assert team_member_user.profile == user_profile
        assert user_profile.user == team_member_user
    
    def test_permission_access_profile_relationship(self, permission_view_projects, access_profile_member):
        """Testa relacionamento entre permissão e perfil de acesso"""
        assert permission_view_projects in access_profile_member.permissions.all()
    
    def test_user_access_profile_relationships(self, user_access_profile, team_member_user, access_profile_member):
        """Testa relacionamentos em UserAccessProfile"""
        # Verificar relacionamento direto
        assert user_access_profile.user == team_member_user
        assert user_access_profile.access_profile == access_profile_member
        
        # Verificar relacionamento reverso
        assert user_access_profile in team_member_user.access_profiles.all()
    
    def test_audit_log_user_relationship(self, audit_log_login, team_member_user):
        """Testa relacionamento entre log de auditoria e usuário"""
        assert audit_log_login.user == team_member_user
        assert audit_log_login in team_member_user.audit_logs.all()


@pytest.mark.django_db
class TestFixtureConsistency:
    """Testes de consistência das fixtures"""
    
    def test_unique_usernames(self, multiple_users):
        """Testa se todos os usuários têm usernames únicos"""
        usernames = [user.username for user in multiple_users]
        assert len(usernames) == len(set(usernames))
    
    def test_unique_emails(self, multiple_users):
        """Testa se todos os usuários têm emails únicos"""
        emails = [user.email for user in multiple_users]
        assert len(emails) == len(set(emails))
    
    def test_password_consistency(self, admin_user, team_member_user):
        """Testa se as senhas estão definidas corretamente"""
        assert admin_user.check_password('adminpass123')
        assert team_member_user.check_password('tmpass123')
        
        # Senhas diferentes não devem funcionar
        assert not admin_user.check_password('wrong_password')
        assert not team_member_user.check_password('wrong_password')
    
    def test_role_consistency(self, admin_user, project_manager_user, team_leader_user, team_member_user, stakeholder_user):
        """Testa se os roles estão definidos corretamente"""
        assert admin_user.role == 'ADMIN'
        assert project_manager_user.role == 'PROJECT_MANAGER'
        assert team_leader_user.role == 'TEAM_LEADER'
        assert team_member_user.role == 'TEAM_MEMBER'
        assert stakeholder_user.role == 'STAKEHOLDER'
