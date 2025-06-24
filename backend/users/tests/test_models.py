"""
Testes para os modelos do módulo Users.
"""
import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.utils import timezone
from datetime import timedelta
from users.models import (
    UserProfile, AccessProfile, Permission, UserAccessProfile,
    PasswordHistory, AuditLog, AccessAttempt, BlacklistedTokens
)

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Testes para o modelo User."""
    
    def test_create_user_valid(self):
        """Testa criação de usuário com dados válidos."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            full_name='Test User',
            password='testpass123'
        )
        
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.full_name == 'Test User'
        assert user.role == 'TEAM_MEMBER'  # Default
        assert user.is_active is True
        assert user.is_staff is False
        assert user.check_password('testpass123')
    
    def test_create_superuser(self):
        """Testa criação de superusuário."""
        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            full_name='Admin User',
            password='adminpass123'
        )
        
        assert user.is_superuser is True
        assert user.is_staff is True
        assert user.is_active is True
        assert user.role == 'ADMIN'
    
    def test_create_user_without_email(self):
        """Testa criação de usuário sem email."""
        with pytest.raises(ValueError, match='Voce Precisa de um endereço de e-mail'):
            User.objects.create_user(
                username='testuser',
                email='',
                full_name='Test User',
                password='testpass123'
            )
    
    def test_create_user_without_username(self):
        """Testa criação de usuário sem username."""
        with pytest.raises(ValueError, match='Users deve ter username'):
            User.objects.create_user(
                username='',
                email='test@example.com',
                full_name='Test User',
                password='testpass123'
            )
    
    def test_create_user_without_full_name(self):
        """Testa criação de usuário sem nome completo."""
        with pytest.raises(ValueError, match='Users deve ter  full name'):
            User.objects.create_user(
                username='testuser',
                email='test@example.com',
                full_name='',
                password='testpass123'
            )
    
    def test_user_str_representation(self, team_member_user):
        """Testa representação string do usuário."""
        assert str(team_member_user) == 'tm_user'
    
    def test_email_normalization(self):
        """Testa normalização do email."""
        user = User.objects.create_user(
            username='testuser',
            email='TEST@EXAMPLE.COM',
            full_name='Test User',
            password='testpass123'
        )
        assert user.email == 'TEST@example.com'
    
    def test_unique_email_constraint(self, team_member_user):
        """Testa constraint de email único."""
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                username='another_user',
                email='tm@example.com',  # Email já usado
                full_name='Another User',
                password='anotherpass123'
            )
    
    def test_unique_username_constraint(self, team_member_user):
        """Testa constraint de username único."""
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                username='tm_user',  # Username já usado
                email='another@example.com',
                full_name='Another User',
                password='anotherpass123'
            )
    
    def test_increment_failed_login(self, team_member_user):
        """Testa incremento de tentativas de login falhadas."""
        initial_attempts = team_member_user.failed_login_attempts
        
        team_member_user.increment_failed_login()
        
        assert team_member_user.failed_login_attempts == initial_attempts + 1
        assert team_member_user.last_login_attempt is not None
    
    def test_lock_account_after_5_attempts(self, team_member_user):
        """Testa bloqueio da conta após 5 tentativas."""
        # Simula 5 tentativas falhadas
        for _ in range(5):
            team_member_user.increment_failed_login()
        
        assert team_member_user.is_locked is True
        assert team_member_user.failed_login_attempts == 5
    
    def test_reset_failed_login(self, locked_user):
        """Testa reset de tentativas de login falhadas."""
        locked_user.reset_failed_login()
        
        assert locked_user.failed_login_attempts == 0
        assert locked_user.is_locked is False
    
    def test_has_permission_admin(self, admin_user):
        """Testa que admin tem todas as permissões."""
        assert admin_user.has_permission('PROJECTS', 'CREATE') is True
        assert admin_user.has_permission('USERS', 'DELETE') is True
    
    def test_has_permission_superuser(self, team_member_user):
        """Testa que superuser tem todas as permissões."""
        team_member_user.is_superuser = True
        team_member_user.save()
        
        assert team_member_user.has_permission('PROJECTS', 'CREATE') is True
    
    def test_has_permission_with_access_profile(self, team_member_user, user_access_profile, permission_view_projects):
        """Testa permissão através de perfil de acesso."""
        assert team_member_user.has_permission('PROJECTS', 'VIEW') is True
        assert team_member_user.has_permission('PROJECTS', 'CREATE') is False
    
    def test_locked_property(self, team_member_user):
        """Testa propriedade locked."""
        assert team_member_user.locked is False
        
        team_member_user.locked = True
        assert team_member_user.is_locked is True
    
    def test_role_choices(self):
        """Testa que todos os papéis esperados estão disponíveis."""
        expected_roles = ['ADMIN', 'PROJECT_MANAGER', 'TEAM_LEADER', 'TEAM_MEMBER', 'STAKEHOLDER', 'AUDITOR']
        available_roles = [choice[0] for choice in User.ROLE_CHOICES]
        
        for role in expected_roles:
            assert role in available_roles
    
    def test_password_change_required_auto_set(self):
        """Testa que last_password_change é definido automaticamente."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            full_name='Test User',
            password='testpass123'
        )
        
        assert user.last_password_change is not None


@pytest.mark.django_db
class TestUserProfileModel:
    """Testes para o modelo UserProfile."""
    
    def test_create_user_profile(self, team_member_user):
        """Testa criação de perfil de usuário."""
        profile = UserProfile.objects.create(
            user=team_member_user,
            phone='+5511999999999',
            theme_preference='DARK',
            email_notifications=False
        )
        
        assert profile.user == team_member_user
        assert profile.phone == '+5511999999999'
        assert profile.theme_preference == 'DARK'
        assert profile.email_notifications is False
        assert profile.system_notifications is True  # Default
    
    def test_user_profile_str(self, user_profile):
        """Testa representação string do perfil."""
        assert str(user_profile) == "tm_user's Profile"
    
    def test_user_profile_one_to_one(self, team_member_user):
        """Testa relacionamento OneToOne com User."""
        profile1 = UserProfile.objects.create(user=team_member_user)
        
        # Tentar criar outro perfil para o mesmo usuário deve dar erro
        with pytest.raises(IntegrityError):
            UserProfile.objects.create(user=team_member_user)
    
    def test_theme_choices(self):
        """Testa opções de tema disponíveis."""
        expected_themes = ['LIGHT', 'DARK', 'SYSTEM']
        available_themes = [choice[0] for choice in UserProfile.THEME_CHOICES]
        
        for theme in expected_themes:
            assert theme in available_themes
    
    def test_profile_defaults(self, team_member_user):
        """Testa valores padrão do perfil."""
        profile = UserProfile.objects.create(user=team_member_user)
        
        assert profile.theme_preference == 'SYSTEM'
        assert profile.email_notifications is True
        assert profile.system_notifications is True
        assert profile.password_change_required is False


@pytest.mark.django_db
class TestAccessProfileModel:
    """Testes para o modelo AccessProfile."""
    
    def test_create_access_profile(self):
        """Testa criação de perfil de acesso."""
        profile = AccessProfile.objects.create(
            name='Test Profile',
            description='Profile for testing'
        )
        
        assert profile.name == 'Test Profile'
        assert profile.description == 'Profile for testing'
        assert profile.created_at is not None
        assert profile.updated_at is not None
    
    def test_access_profile_str(self, access_profile_member):
        """Testa representação string do perfil de acesso."""
        assert str(access_profile_member) == 'Member Profile'
    
    def test_access_profile_without_description(self):
        """Testa criação sem descrição."""
        profile = AccessProfile.objects.create(name='Simple Profile')
        assert profile.description is None


@pytest.mark.django_db
class TestPermissionModel:
    """Testes para o modelo Permission."""
    
    def test_create_permission(self, access_profile_member):
        """Testa criação de permissão."""
        permission = Permission.objects.create(
            access_profile=access_profile_member,
            module='PROJECTS',
            action='VIEW'
        )
        
        assert permission.access_profile == access_profile_member
        assert permission.module == 'PROJECTS'
        assert permission.action == 'VIEW'
    
    def test_permission_str(self, permission_view_projects):
        """Testa representação string da permissão."""
        expected = 'Member Profile - Projects - View'
        assert str(permission_view_projects) == expected
    
    def test_get_action_display(self, permission_view_projects):
        """Testa método get_action_display."""
        assert permission_view_projects.get_action_display() == 'View'
    
    def test_unique_together_constraint(self, access_profile_member):
        """Testa constraint unique_together."""
        # Cria primeira permissão
        Permission.objects.create(
            access_profile=access_profile_member,
            module='PROJECTS',
            action='VIEW'
        )
        
        # Tenta criar permissão duplicada
        with pytest.raises(IntegrityError):
            Permission.objects.create(
                access_profile=access_profile_member,
                module='PROJECTS',
                action='VIEW'
            )
    
    def test_multiple_permissions_same_profile(self, access_profile_member):
        """Testa múltiplas permissões para mesmo perfil."""
        Permission.objects.create(
            access_profile=access_profile_member,
            module='PROJECTS',
            action='VIEW'
        )
        
        Permission.objects.create(
            access_profile=access_profile_member,
            module='PROJECTS',
            action='CREATE'
        )
        
        assert Permission.objects.filter(access_profile=access_profile_member).count() == 2
    
    def test_module_choices(self):
        """Testa módulos disponíveis."""
        expected_modules = [
            'PROJECTS', 'TASKS', 'TEAMS', 'RESOURCES', 'COMMUNICATIONS',
            'RISKS', 'COSTS', 'DOCUMENTS', 'REPORTS', 'USERS', 'SETTINGS',
            'DASHBOARD', 'NOTIFICATIONS', 'APPROVALS'
        ]
        
        available_modules = [choice[0] for choice in Permission.MODULE_CHOICES]
        
        for module in expected_modules:
            assert module in available_modules
    
    def test_action_choices(self):
        """Testa ações disponíveis."""
        expected_actions = [
            'VIEW', 'CREATE', 'EDIT', 'DELETE', 'APPROVE', 'ASSIGN',
            'EXPORT', 'IMPORT', 'COMMENT'
        ]
        
        available_actions = [choice[0] for choice in Permission.ACTION_CHOICES]
        
        for action in expected_actions:
            assert action in available_actions


@pytest.mark.django_db
class TestUserAccessProfileModel:
    """Testes para o modelo UserAccessProfile."""
    
    def test_create_user_access_profile(self, team_member_user, access_profile_member):
        """Testa criação de relacionamento usuário-perfil."""
        user_access = UserAccessProfile.objects.create(
            user=team_member_user,
            access_profile=access_profile_member
        )
        
        assert user_access.user == team_member_user
        assert user_access.access_profile == access_profile_member
    
    def test_user_access_profile_str(self, user_access_profile):
        """Testa representação string."""
        assert str(user_access_profile) == 'tm_user - Member Profile'
    
    def test_unique_together_constraint(self, team_member_user, access_profile_member):
        """Testa constraint unique_together."""
        # Cria primeiro relacionamento
        UserAccessProfile.objects.create(
            user=team_member_user,
            access_profile=access_profile_member
        )
        
        # Tenta criar relacionamento duplicado
        with pytest.raises(IntegrityError):
            UserAccessProfile.objects.create(
                user=team_member_user,
                access_profile=access_profile_member
            )
    
    def test_multiple_profiles_per_user(self, team_member_user, access_profile_member, access_profile_manager):
        """Testa múltiplos perfis para mesmo usuário."""
        UserAccessProfile.objects.create(
            user=team_member_user,
            access_profile=access_profile_member
        )
        
        UserAccessProfile.objects.create(
            user=team_member_user,
            access_profile=access_profile_manager
        )
        
        assert UserAccessProfile.objects.filter(user=team_member_user).count() == 2


@pytest.mark.django_db
class TestPasswordHistoryModel:
    """Testes para o modelo PasswordHistory."""
    
    def test_create_password_history(self, team_member_user):
        """Testa criação de histórico de senha."""
        history = PasswordHistory.objects.create(
            user=team_member_user,
            password_hash='hashed_password_123'
        )
        
        assert history.user == team_member_user
        assert history.password_hash == 'hashed_password_123'
        assert history.created_at is not None
    
    def test_password_history_str(self, password_history):
        """Testa representação string do histórico."""
        expected_pattern = f"{password_history.user.username} - "
        assert str(password_history).startswith(expected_pattern)
    
    def test_password_history_ordering(self, team_member_user):
        """Testa ordenação por data de criação."""
        # Cria dois registros
        history1 = PasswordHistory.objects.create(
            user=team_member_user,
            password_hash='old_hash'
        )
        
        history2 = PasswordHistory.objects.create(
            user=team_member_user,
            password_hash='new_hash'
        )
        
        # Verifica ordenação (mais recente primeiro)
        histories = PasswordHistory.objects.filter(user=team_member_user)
        assert histories.first() == history2
        assert histories.last() == history1


@pytest.mark.django_db
class TestAuditLogModel:
    """Testes para o modelo AuditLog."""
    
    def test_create_audit_log(self, team_member_user):
        """Testa criação de log de auditoria."""
        audit_log = AuditLog.objects.create(
            user=team_member_user,
            action='LOGIN',
            ip_address='192.168.1.100',
            user_agent='Test Browser',
            details={'success': True}
        )
        
        assert audit_log.user == team_member_user
        assert audit_log.action == 'LOGIN'
        assert audit_log.ip_address == '192.168.1.100'
        assert audit_log.details == {'success': True}
    
    def test_audit_log_str(self, audit_log_login):
        """Testa representação string do log."""
        expected_pattern = f"{audit_log_login.user.username} - Login - "
        assert str(audit_log_login).startswith(expected_pattern)
    
    def test_audit_log_action_choices(self):
        """Testa ações disponíveis para auditoria."""
        expected_actions = [
            'LOGIN', 'LOGOUT', 'PASSWORD_CHANGE', 'PASSWORD_RESET_REQUEST',
            'PROFILE_UPDATE', 'PERMISSION_CHANGE', 'ACCOUNT_LOCKED',
            'ACCOUNT_UNLOCKED', 'FAILED_LOGIN', 'USER_CREATED',
            'USER_ACTIVATED', 'USER_DEACTIVATED'
        ]
        
        available_actions = [choice[0] for choice in AuditLog.ACTION_CHOICES]
        
        for action in expected_actions:
            assert action in available_actions


@pytest.mark.django_db
class TestAccessAttemptModel:
    """Testes para o modelo AccessAttempt."""
    
    def test_create_access_attempt(self, team_member_user):
        """Testa criação de tentativa de acesso."""
        attempt = AccessAttempt.objects.create(
            user=team_member_user,
            endpoint='/api/projects/',
            method='GET',
            ip_address='192.168.1.100',
            timestamp=timezone.now(),
            success=True
        )
        
        assert attempt.user == team_member_user
        assert attempt.endpoint == '/api/projects/'
        assert attempt.method == 'GET'
        assert attempt.success is True
    
    def test_access_attempt_str(self, access_attempt_success):
        """Testa representação string da tentativa."""
        expected_pattern = f"{access_attempt_success.user.username} - {access_attempt_success.endpoint} - Success - "
        assert str(access_attempt_success).startswith(expected_pattern)


@pytest.mark.django_db
class TestBlacklistedTokensModel:
    """Testes para o modelo BlacklistedTokens."""
    
    def test_create_blacklisted_token(self, team_member_user):
        """Testa criação de token blacklistado."""
        token = BlacklistedTokens.objects.create(
            token='test.jwt.token',
            user=team_member_user
        )
        
        assert token.token == 'test.jwt.token'
        assert token.user == team_member_user
        assert token.created_at is not None
    
    def test_blacklisted_token_str(self, blacklisted_token):
        """Testa representação string do token."""
        str_repr = str(blacklisted_token)
        assert 'Token' in str_repr
        assert 'blacklisted at' in str_repr
        # Verifica se contém parte do token (primeiros 20 caracteres)
        expected_token_part = blacklisted_token.token[:20]
        assert expected_token_part in str_repr
    
    def test_unique_token_constraint(self, team_member_user):
        """Testa constraint de token único."""
        BlacklistedTokens.objects.create(
            token='unique.token.123',
            user=team_member_user
        )
        
        with pytest.raises(IntegrityError):
            BlacklistedTokens.objects.create(
                token='unique.token.123',  # Token duplicado
                user=team_member_user
            )


@pytest.mark.django_db
class TestModelRelationships:
    """Testes para relacionamentos entre modelos."""
    
    def test_user_profile_cascade_delete(self, team_member_user, user_profile):
        """Testa cascata ao deletar usuário."""
        profile_id = user_profile.id
        team_member_user.delete()
        
        assert not UserProfile.objects.filter(id=profile_id).exists()
    
    def test_user_access_profiles_cascade_delete(self, team_member_user, user_access_profile):
        """Testa cascata de perfis de acesso ao deletar usuário."""
        access_profile_id = user_access_profile.id
        team_member_user.delete()
        
        assert not UserAccessProfile.objects.filter(id=access_profile_id).exists()
    
    def test_permissions_cascade_delete(self, access_profile_member, permission_view_projects):
        """Testa cascata ao deletar perfil de acesso."""
        permission_id = permission_view_projects.id
        access_profile_member.delete()
        
        assert not Permission.objects.filter(id=permission_id).exists()
    
    def test_audit_logs_cascade_delete(self, team_member_user, audit_log_login):
        """Testa cascata de logs ao deletar usuário."""
        log_id = audit_log_login.id
        team_member_user.delete()
        
        assert not AuditLog.objects.filter(id=log_id).exists()
    
    def test_blacklisted_tokens_cascade_delete(self, team_member_user, blacklisted_token):
        """Testa cascata de tokens ao deletar usuário."""
        token_id = blacklisted_token.id
        team_member_user.delete()
        
        assert not BlacklistedTokens.objects.filter(id=token_id).exists()
