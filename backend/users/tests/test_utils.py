"""
Testes para as funções utilitárias do módulo users.
Cobre funções de senha, permissões e request utilities.
"""
import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from unittest.mock import patch, MagicMock
import string

from users.utils import (
    get_client_ip, get_user_agent, generate_secure_password,
    update_user_password, check_user_permission
)
from users.models import (
    UserProfile, AccessProfile, Permission, UserAccessProfile,
    PasswordHistory
)

User = get_user_model()


@pytest.mark.django_db
class TestRequestUtils:
    """Testes para utilitários de request"""
    
    def test_get_client_ip_direct(self):
        """Testa obtenção de IP direto (sem proxy)"""
        factory = RequestFactory()
        request = factory.get('/')
        request.META['REMOTE_ADDR'] = '192.168.1.1'
        
        ip = get_client_ip(request)
        assert ip == '192.168.1.1'
    
    def test_get_client_ip_with_proxy(self):
        """Testa obtenção de IP através de proxy (X-Forwarded-For)"""
        factory = RequestFactory()
        request = factory.get('/')
        request.META['HTTP_X_FORWARDED_FOR'] = '203.0.113.1, 192.168.1.1'
        request.META['REMOTE_ADDR'] = '192.168.1.1'
        
        ip = get_client_ip(request)
        assert ip == '203.0.113.1'  # Primeiro IP da lista
    
    def test_get_client_ip_multiple_proxies(self):
        """Testa obtenção de IP com múltiplos proxies"""
        factory = RequestFactory()
        request = factory.get('/')
        request.META['HTTP_X_FORWARDED_FOR'] = '203.0.113.1, 198.51.100.1, 192.168.1.1'
        
        ip = get_client_ip(request)
        assert ip == '203.0.113.1'  # Primeiro IP (cliente real)
    
    def test_get_user_agent_present(self):
        """Testa obtenção de user agent quando presente"""
        factory = RequestFactory()
        request = factory.get('/')
        user_agent = 'Mozilla/5.0 (Test Browser)'
        request.META['HTTP_USER_AGENT'] = user_agent
        
        result = get_user_agent(request)
        assert result == user_agent
    
    def test_get_user_agent_missing(self):
        """Testa obtenção de user agent quando ausente"""
        factory = RequestFactory()
        request = factory.get('/')
        
        result = get_user_agent(request)
        assert result == ''


@pytest.mark.django_db
class TestPasswordUtils:
    """Testes para utilitários de senha"""
    
    def test_generate_secure_password_default_length(self):
        """Testa geração de senha segura com tamanho padrão"""
        password = generate_secure_password()
        
        assert len(password) == 12  # Tamanho padrão
        assert isinstance(password, str)
    
    def test_generate_secure_password_custom_length(self):
        """Testa geração de senha segura com tamanho customizado"""
        length = 16
        password = generate_secure_password(length)
        
        assert len(password) == length
    
    def test_generate_secure_password_complexity(self):
        """Testa complexidade da senha gerada"""
        password = generate_secure_password(12)
        
        # Verificar se contém pelo menos um de cada tipo
        has_lowercase = any(c in string.ascii_lowercase for c in password)
        has_uppercase = any(c in string.ascii_uppercase for c in password)
        has_digit = any(c in string.digits for c in password)
        has_special = any(c in '!@#$%^&*(),.?":{}|<>' for c in password)
        
        assert has_lowercase, "Senha deve conter ao menos uma letra minúscula"
        assert has_uppercase, "Senha deve conter ao menos uma letra maiúscula"
        assert has_digit, "Senha deve conter ao menos um dígito"
        assert has_special, "Senha deve conter ao menos um caractere especial"
    
    def test_generate_secure_password_uniqueness(self):
        """Testa se senhas geradas são únicas"""
        passwords = [generate_secure_password() for _ in range(10)]
        
        # Todas as senhas devem ser diferentes
        assert len(set(passwords)) == len(passwords)
    
    def test_update_user_password_success(self, team_member_user):
        """Testa atualização de senha com sucesso"""
        new_password = 'NewSecurePass123!'
        
        result = update_user_password(team_member_user, new_password)
        
        assert result == team_member_user
        assert team_member_user.check_password(new_password)
    
    def test_update_user_password_invalid_user(self):
        """Testa atualização de senha com usuário inválido"""
        with pytest.raises(ValueError, match="Usuário é obrigatório"):
            update_user_password(None, 'password')
    
    def test_update_user_password_invalid_password(self, team_member_user):
        """Testa atualização de senha com senha inválida"""
        with pytest.raises(ValueError, match="Nova senha é obrigatória"):
            update_user_password(team_member_user, None)
        
        with pytest.raises(ValueError, match="Nova senha é obrigatória"):
            update_user_password(team_member_user, '')
    
    def test_update_user_password_creates_history(self, team_member_user):
        """Testa se atualização de senha cria histórico"""
        # Definir senha inicial
        initial_password = 'InitialPass123!'
        team_member_user.set_password(initial_password)
        team_member_user.save()
        
        initial_hash = team_member_user.password
        
        # Atualizar senha
        new_password = 'NewSecurePass123!'
        update_user_password(team_member_user, new_password)
        
        # Verificar se histórico foi criado
        history = PasswordHistory.objects.filter(user=team_member_user).first()
        assert history is not None
        assert history.password_hash == initial_hash
    
    def test_update_user_password_limits_history(self, team_member_user):
        """Testa se histórico de senhas é limitado a 5 registros"""
        # Criar usuário com senha inicial
        team_member_user.set_password('InitialPass123!')
        team_member_user.save()
        
        # Alterar senha 6 vezes para testar o limite
        for i in range(6):
            new_password = f'Password{i}123!'
            update_user_password(team_member_user, new_password)
        
        # Verificar se apenas 5 históricos foram mantidos
        history_count = PasswordHistory.objects.filter(user=team_member_user).count()
        assert history_count <= 5
    
    @patch('users.utils.logger')
    def test_update_user_password_logs_success(self, mock_logger, team_member_user):
        """Testa se atualização de senha gera log de sucesso"""
        new_password = 'NewSecurePass123!'
        
        update_user_password(team_member_user, new_password)
        
        mock_logger.info.assert_called()
        call_args = mock_logger.info.call_args[0][0]
        assert 'Senha alterada para o usuário' in call_args
        assert team_member_user.username in call_args
    
    @patch('users.utils.logger')
    def test_update_user_password_handles_history_error(self, mock_logger, team_member_user):
        """Testa tratamento de erro ao salvar histórico"""
        # Simular erro no modelo PasswordHistory diretamente
        from users.models import PasswordHistory
        
        with patch.object(PasswordHistory.objects, 'create', side_effect=Exception('DB Error')):
            new_password = 'NewSecurePass123!'
            
            # Deve ainda funcionar mesmo com erro no histórico
            result = update_user_password(team_member_user, new_password)
            
            assert result == team_member_user
            assert team_member_user.check_password(new_password)
            mock_logger.warning.assert_called()


@pytest.mark.django_db
class TestPermissionUtils:
    """Testes para utilitários de permissões"""
    
    def test_check_user_permission_superuser(self, admin_user):
        """Testa verificação de permissão para superusuário"""
        admin_user.is_superuser = True
        admin_user.save()
        
        result = check_user_permission(admin_user, 'PROJECTS', 'DELETE')
        assert result is True
    
    def test_check_user_permission_admin_role(self, admin_user):
        """Testa verificação de permissão para role ADMIN"""
        admin_user.role = 'ADMIN'
        admin_user.save()
        
        result = check_user_permission(admin_user, 'PROJECTS', 'DELETE')
        assert result is True
    
    def test_check_user_permission_with_access_profile(self, team_member_user):
        """Testa verificação de permissão através de perfil de acesso"""
        # Criar perfil de acesso
        access_profile = AccessProfile.objects.create(
            name='Project Manager',
            description='Can manage projects'
        )
        
        # Criar permissão
        Permission.objects.create(
            access_profile=access_profile,
            module='PROJECTS',
            action='EDIT'
        )
        
        # Atribuir perfil ao usuário
        UserAccessProfile.objects.create(
            user=team_member_user,
            access_profile=access_profile
        )
        
        # Verificar permissão existente
        result = check_user_permission(team_member_user, 'PROJECTS', 'EDIT')
        assert result is True
        
        # Verificar permissão inexistente
        result = check_user_permission(team_member_user, 'PROJECTS', 'DELETE')
        assert result is False
    
    def test_check_user_permission_multiple_profiles(self, team_member_user):
        """Testa verificação de permissão com múltiplos perfis"""
        # Criar dois perfis
        profile1 = AccessProfile.objects.create(name='Profile 1')
        profile2 = AccessProfile.objects.create(name='Profile 2')
        
        # Criar permissões em perfis diferentes
        Permission.objects.create(
            access_profile=profile1,
            module='PROJECTS',
            action='VIEW'
        )
        Permission.objects.create(
            access_profile=profile2,
            module='TASKS',
            action='EDIT'
        )
        
        # Atribuir ambos os perfis
        UserAccessProfile.objects.create(user=team_member_user, access_profile=profile1)
        UserAccessProfile.objects.create(user=team_member_user, access_profile=profile2)
        
        # Verificar permissões de ambos os perfis
        assert check_user_permission(team_member_user, 'PROJECTS', 'VIEW') is True
        assert check_user_permission(team_member_user, 'TASKS', 'EDIT') is True
        assert check_user_permission(team_member_user, 'USERS', 'DELETE') is False
    
    def test_check_user_permission_no_profiles(self, team_member_user):
        """Testa verificação de permissão para usuário sem perfis"""
        result = check_user_permission(team_member_user, 'PROJECTS', 'VIEW')
        assert result is False
    
    @patch('users.utils.logger')
    def test_check_user_permission_handles_exception(self, mock_logger, team_member_user):
        """Testa tratamento de exceção na verificação de permissão"""
        # Simular erro no modelo UserAccessProfile diretamente
        from users.models import UserAccessProfile
        
        with patch.object(UserAccessProfile.objects, 'filter', side_effect=Exception('DB Error')):
            result = check_user_permission(team_member_user, 'PROJECTS', 'VIEW')
            
            # Deve retornar False em caso de erro
            assert result is False
            # O log deve ser warning, não error
            mock_logger.warning.assert_called()


@pytest.mark.django_db
class TestUtilsIntegration:
    """Testes de integração dos utilitários"""
    
    def test_password_and_permission_flow(self, team_member_user):
        """Testa fluxo integrado de senha e permissões"""
        # 1. Atualizar senha
        new_password = generate_secure_password(16)
        update_user_password(team_member_user, new_password)
        
        # 2. Verificar se senha foi atualizada
        assert team_member_user.check_password(new_password)
        
        # 3. Criar permissões
        access_profile = AccessProfile.objects.create(name='Test Profile')
        Permission.objects.create(
            access_profile=access_profile,
            module='PROJECTS',
            action='VIEW'
        )
        UserAccessProfile.objects.create(
            user=team_member_user,
            access_profile=access_profile
        )
        
        # 4. Verificar permissões
        assert check_user_permission(team_member_user, 'PROJECTS', 'VIEW') is True
    
    def test_request_utils_with_real_scenario(self):
        """Testa utilitários de request em cenário real"""
        factory = RequestFactory()
        
        # Simular request real com headers
        request = factory.post('/api/users/login/')
        request.META.update({
            'HTTP_X_FORWARDED_FOR': '203.0.113.1, 192.168.1.1',
            'REMOTE_ADDR': '192.168.1.1',
            'HTTP_USER_AGENT': 'Mozilla/5.0 (Test Browser) AppleWebKit/537.36'
        })
        
        ip = get_client_ip(request)
        user_agent = get_user_agent(request)
        
        assert ip == '203.0.113.1'
        assert 'Mozilla/5.0' in user_agent
        assert 'AppleWebKit' in user_agent


@pytest.mark.django_db
class TestUtilsEdgeCases:
    """Testes de casos extremos para utilitários"""
    
    def test_generate_password_minimum_length(self):
        """Testa geração de senha com tamanho mínimo"""
        # Tamanho menor que 4 deve ainda garantir complexidade
        password = generate_secure_password(4)
        assert len(password) == 4
    
    def test_generate_password_large_length(self):
        """Testa geração de senha com tamanho grande"""
        password = generate_secure_password(100)
        assert len(password) == 100
    
    def test_update_password_with_special_characters(self, team_member_user):
        """Testa atualização de senha com caracteres especiais"""
        special_password = 'P@ssw0rd!#$%^&*()_+-=[]{}|;:,.<>?'
        
        result = update_user_password(team_member_user, special_password)
        
        assert result == team_member_user
        assert team_member_user.check_password(special_password)
    
    def test_check_permission_case_sensitivity(self, team_member_user):
        """Testa sensibilidade a maiúsculas/minúsculas nas permissões"""
        access_profile = AccessProfile.objects.create(name='Test Profile')
        Permission.objects.create(
            access_profile=access_profile,
            module='PROJECTS',
            action='VIEW'
        )
        UserAccessProfile.objects.create(
            user=team_member_user,
            access_profile=access_profile
        )
        
        # Permissão deve ser case-sensitive
        assert check_user_permission(team_member_user, 'PROJECTS', 'VIEW') is True
        assert check_user_permission(team_member_user, 'projects', 'view') is False
        assert check_user_permission(team_member_user, 'Projects', 'View') is False
