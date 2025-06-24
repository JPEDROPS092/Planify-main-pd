# users/tests/test_security.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch, MagicMock
from users.validators import PasswordPolicyValidator, validate_username, validate_full_name
from users.utils import (
    generate_secure_password, get_client_ip, lock_user_account,
    unlock_user_account, is_account_locked
)
from users.security_notifications import SecurityNotificationService
from users.audit import create_audit_log, AuditLog
import re

User = get_user_model()


class PasswordValidatorTest(TestCase):
    """Testes para validador de política de senhas"""
    
    def setUp(self):
        self.validator = PasswordPolicyValidator()
        self.user = User(
            username='testuser',
            email='test@example.com',
            full_name='Test User'
        )
    
    def test_valid_password(self):
        """Testa senha válida"""
        valid_password = 'SecurePass123!'
        
        # Não deve levantar exceção
        try:
            self.validator.validate(valid_password, self.user)
        except ValidationError:
            self.fail("validate() levantou ValidationError inesperadamente!")
    
    def test_password_too_short(self):
        """Testa senha muito curta"""
        short_password = '123'
        
        with self.assertRaises(ValidationError) as context:
            self.validator.validate(short_password, self.user)
        
        self.assertIn('pelo menos 8 caracteres', str(context.exception))
    
    def test_password_too_long(self):
        """Testa senha muito longa"""
        long_password = 'a' * 150
        
        with self.assertRaises(ValidationError) as context:
            self.validator.validate(long_password, self.user)
        
        self.assertIn('no máximo 128 caracteres', str(context.exception))
    
    def test_password_missing_uppercase(self):
        """Testa senha sem letra maiúscula"""
        password = 'securepass123!'
        
        with self.assertRaises(ValidationError) as context:
            self.validator.validate(password, self.user)
        
        self.assertIn('letra maiúscula', str(context.exception))
    
    def test_password_missing_lowercase(self):
        """Testa senha sem letra minúscula"""
        password = 'SECUREPASS123!'
        
        with self.assertRaises(ValidationError) as context:
            self.validator.validate(password, self.user)
        
        self.assertIn('letra minúscula', str(context.exception))
    
    def test_password_missing_numbers(self):
        """Testa senha sem números"""
        password = 'SecurePass!'
        
        with self.assertRaises(ValidationError) as context:
            self.validator.validate(password, self.user)
        
        self.assertIn('pelo menos um número', str(context.exception))
    
    def test_password_missing_special_chars(self):
        """Testa senha sem caracteres especiais"""
        password = 'SecurePass123'
        
        with self.assertRaises(ValidationError) as context:
            self.validator.validate(password, self.user)
        
        self.assertIn('caractere especial', str(context.exception))
    
    def test_common_password(self):
        """Testa senha comum"""
        common_password = 'Password123!'
        
        with self.assertRaises(ValidationError) as context:
            self.validator.validate(common_password, self.user)
        
        self.assertIn('muito comum', str(context.exception))
    
    def test_password_contains_user_info(self):
        """Testa senha que contém informações do usuário"""
        password = 'TestuserPass123!'
        
        with self.assertRaises(ValidationError) as context:
            self.validator.validate(password, self.user)
        
        self.assertIn('informações pessoais', str(context.exception))
    
    def test_password_contains_email_part(self):
        """Testa senha que contém parte do email"""
        password = 'TestPass123!'
        
        with self.assertRaises(ValidationError) as context:
            self.validator.validate(password, self.user)
        
        self.assertIn('informações pessoais', str(context.exception))
    
    def test_get_help_text(self):
        """Testa texto de ajuda"""
        help_text = self.validator.get_help_text()
        
        self.assertIn('8 e 128 caracteres', help_text)
        self.assertIn('letra maiúscula', help_text)
        self.assertIn('letra minúscula', help_text)
        self.assertIn('número', help_text)
        self.assertIn('caractere especial', help_text)


class UsernameValidatorTest(TestCase):
    """Testes para validador de username"""
    
    def test_valid_username(self):
        """Testa username válido"""
        valid_usernames = ['user123', 'test_user', 'user-name', 'user.name']
        
        for username in valid_usernames:
            try:
                validate_username(username)
            except ValidationError:
                self.fail(f"validate_username() levantou ValidationError para '{username}'")
    
    def test_username_too_short(self):
        """Testa username muito curto"""
        with self.assertRaises(ValidationError) as context:
            validate_username('ab')
        
        self.assertIn('pelo menos 3 caracteres', str(context.exception))
    
    def test_username_too_long(self):
        """Testa username muito longo"""
        long_username = 'a' * 31
        
        with self.assertRaises(ValidationError) as context:
            validate_username(long_username)
        
        self.assertIn('no máximo 30 caracteres', str(context.exception))
    
    def test_username_invalid_characters(self):
        """Testa username com caracteres inválidos"""
        invalid_usernames = ['user@name', 'user name', 'user#name', 'user$name']
        
        for username in invalid_usernames:
            with self.assertRaises(ValidationError):
                validate_username(username)
    
    def test_username_starts_with_special(self):
        """Testa username que começa com caractere especial"""
        invalid_usernames = ['.username', '-username', '_username']
        
        for username in invalid_usernames:
            with self.assertRaises(ValidationError) as context:
                validate_username(username)
            
            self.assertIn('não pode começar', str(context.exception))
    
    def test_username_reserved(self):
        """Testa username reservado"""
        reserved_usernames = ['admin', 'root', 'api', 'system']
        
        for username in reserved_usernames:
            with self.assertRaises(ValidationError) as context:
                validate_username(username)
            
            self.assertIn('reservado', str(context.exception))


class FullNameValidatorTest(TestCase):
    """Testes para validador de nome completo"""
    
    def test_valid_full_name(self):
        """Testa nome completo válido"""
        valid_names = [
            'João Silva',
            'Maria dos Santos',
            'José da Silva-Junior',
            "O'Connor",
            'Ana Lúcia',
            'Carlos M. Santos'
        ]
        
        for name in valid_names:
            try:
                validate_full_name(name)
            except ValidationError:
                self.fail(f"validate_full_name() levantou ValidationError para '{name}'")
    
    def test_full_name_too_short(self):
        """Testa nome muito curto"""
        with self.assertRaises(ValidationError) as context:
            validate_full_name('A')
        
        self.assertIn('pelo menos 2 caracteres', str(context.exception))
    
    def test_full_name_too_long(self):
        """Testa nome muito longo"""
        long_name = 'A' * 101
        
        with self.assertRaises(ValidationError) as context:
            validate_full_name(long_name)
        
        self.assertIn('no máximo 100 caracteres', str(context.exception))
    
    def test_full_name_invalid_characters(self):
        """Testa nome com caracteres inválidos"""
        invalid_names = ['João123', 'Maria@Silva', 'José#Santos', 'Ana$Costa']
        
        for name in invalid_names:
            with self.assertRaises(ValidationError):
                validate_full_name(name)


class SecurityUtilsTest(TestCase):
    """Testes para utilitários de segurança"""
    
    def test_generate_secure_password(self):
        """Testa geração de senha segura"""
        password = generate_secure_password()
        
        # Verificar comprimento
        self.assertEqual(len(password), 12)
        
        # Verificar se contém pelo menos um de cada tipo
        self.assertTrue(re.search(r'[a-z]', password))  # minúscula
        self.assertTrue(re.search(r'[A-Z]', password))  # maiúscula
        self.assertTrue(re.search(r'\d', password))     # número
        self.assertTrue(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))  # especial
    
    def test_generate_secure_password_custom_length(self):
        """Testa geração de senha com comprimento customizado"""
        password = generate_secure_password(16)
        self.assertEqual(len(password), 16)
    
    def test_get_client_ip_with_forwarded(self):
        """Testa obtenção de IP com X-Forwarded-For"""
        mock_request = MagicMock()
        mock_request.META = {
            'HTTP_X_FORWARDED_FOR': '192.168.1.1, 10.0.0.1',
            'REMOTE_ADDR': '127.0.0.1'
        }
        
        ip = get_client_ip(mock_request)
        self.assertEqual(ip, '192.168.1.1')
    
    def test_get_client_ip_without_forwarded(self):
        """Testa obtenção de IP sem X-Forwarded-For"""
        mock_request = MagicMock()
        mock_request.META = {
            'REMOTE_ADDR': '127.0.0.1'
        }
        
        ip = get_client_ip(mock_request)
        self.assertEqual(ip, '127.0.0.1')


class AccountLockingTest(TestCase):
    """Testes para sistema de bloqueio de conta"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            full_name='Test User',
            password='TestPass123!'
        )
    
    def test_lock_user_account(self):
        """Testa bloqueio de conta"""
        lock_user_account(self.user, 'Test reason')
        
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_locked)
        self.assertIsNotNone(self.user.locked_until)
    
    def test_unlock_user_account(self):
        """Testa desbloqueio de conta"""
        # Primeiro bloquear
        self.user.is_locked = True
        self.user.failed_login_attempts = 5
        self.user.save()
        
        # Depois desbloquear
        unlock_user_account(self.user)
        
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_locked)
        self.assertIsNone(self.user.locked_until)
        self.assertEqual(self.user.failed_login_attempts, 0)
    
    def test_is_account_locked_true(self):
        """Testa verificação de conta bloqueada"""
        self.user.is_locked = True
        self.user.save()
        
        self.assertTrue(is_account_locked(self.user))
    
    def test_is_account_locked_false(self):
        """Testa verificação de conta não bloqueada"""
        self.assertFalse(is_account_locked(self.user))
    
    def test_is_account_locked_expired(self):
        """Testa desbloqueio automático de conta com bloqueio expirado"""
        past_time = timezone.now() - timedelta(hours=1)
        self.user.is_locked = True
        self.user.locked_until = past_time
        self.user.save()
        
        # Deve desbloquear automaticamente
        self.assertFalse(is_account_locked(self.user))
        
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_locked)


class SecurityNotificationTest(TestCase):
    """Testes para notificações de segurança"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            full_name='Test User',
            password='TestPass123!'
        )
    
    @patch('users.security_notifications.send_mail')
    def test_notify_password_change(self, mock_send_mail):
        """Testa notificação de alteração de senha"""
        mock_send_mail.return_value = True
        
        result = SecurityNotificationService.notify_password_change(
            self.user, '192.168.1.1'
        )
        
        self.assertTrue(result)
        mock_send_mail.assert_called_once()
        
        # Verificar argumentos da chamada
        call_args = mock_send_mail.call_args
        self.assertIn('Senha alterada', call_args[1]['subject'])
        self.assertEqual(call_args[1]['recipient_list'], [self.user.email])
    
    @patch('users.security_notifications.send_mail')
    def test_notify_suspicious_login(self, mock_send_mail):
        """Testa notificação de login suspeito"""
        mock_send_mail.return_value = True
        
        result = SecurityNotificationService.notify_suspicious_login(
            self.user, '192.168.1.1', 'Mozilla/5.0...'
        )
        
        self.assertTrue(result)
        mock_send_mail.assert_called_once()
        
        call_args = mock_send_mail.call_args
        self.assertIn('suspeita', call_args[1]['subject'])
    
    @patch('users.security_notifications.send_mail')
    def test_notify_account_locked(self, mock_send_mail):
        """Testa notificação de conta bloqueada"""
        mock_send_mail.return_value = True
        
        result = SecurityNotificationService.notify_account_locked(self.user)
        
        self.assertTrue(result)
        mock_send_mail.assert_called_once()
        
        call_args = mock_send_mail.call_args
        self.assertIn('bloqueada', call_args[1]['subject'])
    
    @patch('users.security_notifications.send_mail')
    def test_notify_account_unlocked(self, mock_send_mail):
        """Testa notificação de conta desbloqueada"""
        mock_send_mail.return_value = True
        
        result = SecurityNotificationService.notify_account_unlocked(self.user)
        
        self.assertTrue(result)
        mock_send_mail.assert_called_once()
        
        call_args = mock_send_mail.call_args
        self.assertIn('desbloqueada', call_args[1]['subject'])


class AuditLogTest(TestCase):
    """Testes para sistema de auditoria"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            full_name='Test User',
            password='TestPass123!'
        )
    
    def test_create_audit_log(self):
        """Testa criação de log de auditoria"""
        log = create_audit_log(
            user=self.user,
            action='LOGIN',
            ip_address='192.168.1.1',
            user_agent='Mozilla/5.0...',
            details={'success': True}
        )
        
        self.assertIsInstance(log, AuditLog)
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.action, 'LOGIN')
        self.assertEqual(log.ip_address, '192.168.1.1')
        self.assertEqual(log.details, {'success': True})
    
    def test_audit_log_ordering(self):
        """Testa ordenação dos logs de auditoria"""
        log1 = create_audit_log(self.user, 'LOGIN')
        log2 = create_audit_log(self.user, 'LOGOUT')
        
        logs = AuditLog.objects.all()
        self.assertEqual(logs.first(), log2)  # Mais recente primeiro
        self.assertEqual(logs.last(), log1)
    
    def test_audit_log_str_representation(self):
        """Testa representação string do log"""
        log = create_audit_log(self.user, 'LOGIN')
        
        str_repr = str(log)
        self.assertIn('testuser', str_repr)
        self.assertIn('Login', str_repr)


class FailedLoginAttemptsTest(TestCase):
    """Testes para tentativas falhadas de login"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            full_name='Test User',
            password='TestPass123!'
        )
    
    def test_increment_failed_login_attempts(self):
        """Testa incremento de tentativas falhadas"""
        self.assertEqual(self.user.failed_login_attempts, 0)
        
        self.user.increment_failed_login()
        self.assertEqual(self.user.failed_login_attempts, 1)
        self.assertIsNotNone(self.user.last_login_attempt)
    
    def test_account_locks_after_max_attempts(self):
        """Testa bloqueio após máximo de tentativas"""
        for i in range(5):
            self.user.increment_failed_login()
        
        self.assertTrue(self.user.is_locked)
        self.assertEqual(self.user.failed_login_attempts, 5)
    
    def test_reset_failed_login_attempts(self):
        """Testa reset de tentativas falhadas"""
        # Simular tentativas falhadas
        for i in range(3):
            self.user.increment_failed_login()
        
        self.assertEqual(self.user.failed_login_attempts, 3)
        
        # Reset
        self.user.reset_failed_login()
        self.assertEqual(self.user.failed_login_attempts, 0)
        self.assertFalse(self.user.is_locked)
