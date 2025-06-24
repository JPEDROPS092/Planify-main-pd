# users/tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from users.models import (
    UserProfile, AccessProfile, Permission, 
    UserAccessProfile, BlacklistedTokens, PasswordHistory, AuditLog
)

User = get_user_model()


class UserModelTest(TestCase):
    """Testes para o modelo User"""
    
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'full_name': 'Test User',
            'password': 'SecurePass123!'
        }
    
    def test_create_user(self):
        """Testa criação de usuário"""
        user = User.objects.create_user(**self.user_data)
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.full_name, 'Test User')
        self.assertEqual(user.role, 'TEAM_MEMBER')  # Valor padrão
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password('SecurePass123!'))
    
    def test_create_superuser(self):
        """Testa criação de superusuário"""
        user = User.objects.create_superuser(**self.user_data)
        
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertEqual(user.role, 'ADMIN')
    
    def test_user_str_representation(self):
        """Testa representação string do usuário"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'testuser')
    
    def test_user_uuid_generation(self):
        """Testa geração automática de UUID"""
        user = User.objects.create_user(**self.user_data)
        self.assertIsNotNone(user.uuid)
        
        # Criar outro usuário e verificar que UUID é único
        user2_data = self.user_data.copy()
        user2_data['username'] = 'testuser2'
        user2_data['email'] = 'test2@example.com'
        user2 = User.objects.create_user(**user2_data)
        
        self.assertNotEqual(user.uuid, user2.uuid)
    
    def test_increment_failed_login(self):
        """Testa incremento de tentativas falhadas de login"""
        user = User.objects.create_user(**self.user_data)
        
        # Primeira tentativa falha
        user.increment_failed_login()
        self.assertEqual(user.failed_login_attempts, 1)
        self.assertFalse(user.is_locked)
        
        # Incrementar até atingir o limite
        for i in range(4):
            user.increment_failed_login()
        
        self.assertEqual(user.failed_login_attempts, 5)
        self.assertTrue(user.is_locked)
    
    def test_reset_failed_login(self):
        """Testa reset de tentativas falhadas de login"""
        user = User.objects.create_user(**self.user_data)
        
        # Simular tentativas falhadas
        for i in range(5):
            user.increment_failed_login()
        
        self.assertTrue(user.is_locked)
        
        # Reset
        user.reset_failed_login()
        self.assertEqual(user.failed_login_attempts, 0)
        self.assertFalse(user.is_locked)
    
    def test_has_permission_admin(self):
        """Testa permissões para administrador"""
        user = User.objects.create_user(**self.user_data)
        user.role = 'ADMIN'
        user.save()
        
        # Admin deve ter todas as permissões
        self.assertTrue(user.has_permission('PROJECTS', 'CREATE'))
        self.assertTrue(user.has_permission('USERS', 'DELETE'))
    
    def test_has_permission_superuser(self):
        """Testa permissões para superusuário"""
        user = User.objects.create_superuser(**self.user_data)
        
        # Superuser deve ter todas as permissões
        self.assertTrue(user.has_permission('PROJECTS', 'CREATE'))
        self.assertTrue(user.has_permission('USERS', 'DELETE'))


class UserProfileModelTest(TestCase):
    """Testes para o modelo UserProfile"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            full_name='Test User',
            password='SecurePass123!'
        )
    
    def test_create_user_profile(self):
        """Testa criação de perfil de usuário"""
        profile = UserProfile.objects.create(
            user=self.user,
            phone='11999999999',
            theme_preference='DARK',
            email_notifications=False
        )
        
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.phone, '11999999999')
        self.assertEqual(profile.theme_preference, 'DARK')
        self.assertFalse(profile.email_notifications)
        self.assertTrue(profile.system_notifications)  # Valor padrão
    
    def test_user_profile_str_representation(self):
        """Testa representação string do perfil"""
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(str(profile), "testuser's Profile")


class AccessProfileModelTest(TestCase):
    """Testes para o modelo AccessProfile"""
    
    def test_create_access_profile(self):
        """Testa criação de perfil de acesso"""
        profile = AccessProfile.objects.create(
            name='Project Manager',
            description='Gerente de projetos com acesso completo a projetos'
        )
        
        self.assertEqual(profile.name, 'Project Manager')
        self.assertIsNotNone(profile.created_at)
        self.assertIsNotNone(profile.updated_at)
    
    def test_access_profile_str_representation(self):
        """Testa representação string do perfil de acesso"""
        profile = AccessProfile.objects.create(name='Test Profile')
        self.assertEqual(str(profile), 'Test Profile')


class PermissionModelTest(TestCase):
    """Testes para o modelo Permission"""
    
    def setUp(self):
        self.access_profile = AccessProfile.objects.create(
            name='Test Profile'
        )
    
    def test_create_permission(self):
        """Testa criação de permissão"""
        permission = Permission.objects.create(
            access_profile=self.access_profile,
            module='PROJECTS',
            action='CREATE'
        )
        
        self.assertEqual(permission.access_profile, self.access_profile)
        self.assertEqual(permission.module, 'PROJECTS')
        self.assertEqual(permission.action, 'CREATE')
    
    def test_permission_str_representation(self):
        """Testa representação string da permissão"""
        permission = Permission.objects.create(
            access_profile=self.access_profile,
            module='PROJECTS',
            action='CREATE'
        )
        
        expected_str = f"{self.access_profile.name} - Projects - Create"
        self.assertEqual(str(permission), expected_str)
    
    def test_unique_together_constraint(self):
        """Testa constraint de unicidade"""
        Permission.objects.create(
            access_profile=self.access_profile,
            module='PROJECTS',
            action='CREATE'
        )
        
        # Tentar criar permissão duplicada deve gerar erro
        with self.assertRaises(Exception):
            Permission.objects.create(
                access_profile=self.access_profile,
                module='PROJECTS',
                action='CREATE'
            )


class BlacklistedTokensModelTest(TestCase):
    """Testes para o modelo BlacklistedTokens"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            full_name='Test User',
            password='SecurePass123!'
        )
    
    def test_create_blacklisted_token(self):
        """Testa criação de token blacklisted"""
        token = BlacklistedTokens.objects.create(
            token='test.jwt.token',
            user=self.user
        )
        
        self.assertEqual(token.token, 'test.jwt.token')
        self.assertEqual(token.user, self.user)
        self.assertIsNotNone(token.created_at)
    
    def test_blacklisted_token_str_representation(self):
        """Testa representação string do token blacklisted"""
        token = BlacklistedTokens.objects.create(
            token='test.jwt.token.very.long.string',
            user=self.user
        )
        
        # Deve mostrar apenas os primeiros 20 caracteres
        self.assertTrue(str(token).startswith('Token test.jwt.token.very'))
        self.assertTrue('blacklisted at' in str(token))


class PasswordHistoryModelTest(TestCase):
    """Testes para o modelo PasswordHistory"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            full_name='Test User',
            password='SecurePass123!'
        )
    
    def test_create_password_history(self):
        """Testa criação de histórico de senha"""
        history = PasswordHistory.objects.create(
            user=self.user,
            password_hash='hashed_password_string'
        )
        
        self.assertEqual(history.user, self.user)
        self.assertEqual(history.password_hash, 'hashed_password_string')
        self.assertIsNotNone(history.created_at)
    
    def test_password_history_ordering(self):
        """Testa ordenação do histórico de senhas"""
        # Criar múltiplos registros
        history1 = PasswordHistory.objects.create(
            user=self.user,
            password_hash='hash1'
        )
        history2 = PasswordHistory.objects.create(
            user=self.user,
            password_hash='hash2'
        )
        
        # O mais recente deve vir primeiro
        histories = PasswordHistory.objects.filter(user=self.user)
        self.assertEqual(histories.first(), history2)
        self.assertEqual(histories.last(), history1)


class AuditLogModelTest(TestCase):
    """Testes para o modelo AuditLog"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            full_name='Test User',
            password='SecurePass123!'
        )
    
    def test_create_audit_log(self):
        """Testa criação de log de auditoria"""
        log = AuditLog.objects.create(
            user=self.user,
            action='LOGIN',
            ip_address='192.168.1.1',
            user_agent='Mozilla/5.0...',
            details={'success': True}
        )
        
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.action, 'LOGIN')
        self.assertEqual(log.ip_address, '192.168.1.1')
        self.assertEqual(log.details, {'success': True})
        self.assertIsNotNone(log.timestamp)
    
    def test_audit_log_str_representation(self):
        """Testa representação string do log de auditoria"""
        log = AuditLog.objects.create(
            user=self.user,
            action='LOGIN',
            ip_address='192.168.1.1'
        )
        
        str_repr = str(log)
        self.assertIn('testuser', str_repr)
        self.assertIn('Login', str_repr)
        self.assertIn(log.timestamp.strftime('%Y-%m-%d %H:%M:%S'), str_repr)
