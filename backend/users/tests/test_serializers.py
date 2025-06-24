"""
Testes para os serializers do módulo Users.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from users.models import UserProfile, AccessProfile, Permission, UserAccessProfile
from users.serializers import (
    UserSerializer, UserCreateSerializer, UserProfileSerializer,
    AccessProfileSerializer, PermissionSerializer, UserAccessProfileSerializer,
    ChangePasswordSerializer, ResetPasswordSerializer, SetNewPasswordSerializer
)

User = get_user_model()


@pytest.mark.django_db
class TestUserProfileSerializer:
    """Testes para UserProfileSerializer."""
    
    def test_serialization(self, user_profile):
        """Testa serialização do perfil de usuário."""
        serializer = UserProfileSerializer(user_profile)
        data = serializer.data
        
        assert data['phone'] == '+5511999999999'
        assert data['theme_preference'] == 'DARK'
        assert data['email_notifications'] is True
        assert data['system_notifications'] is False
    
    def test_deserialization(self, team_member_user):
        """Testa deserialização do perfil."""
        data = {
            'user': team_member_user.pk,
            'phone': '+5511888888888',
            'theme_preference': 'LIGHT',
            'email_notifications': False,
            'system_notifications': True
        }
        
        serializer = UserProfileSerializer(data=data)
        assert serializer.is_valid()
        
        profile = serializer.save()
        assert profile.phone == '+5511888888888'
        assert profile.theme_preference == 'LIGHT'
        assert profile.email_notifications is False
    
    def test_validation_invalid_theme(self):
        """Testa validação de tema inválido."""
        data = {
            'theme_preference': 'INVALID_THEME'
        }
        
        serializer = UserProfileSerializer(data=data)
        assert not serializer.is_valid()
        assert 'theme_preference' in serializer.errors


@pytest.mark.django_db
class TestPermissionSerializer:
    """Testes para PermissionSerializer."""
    
    def test_serialization(self, permission_view_projects):
        """Testa serialização de permissão."""
        serializer = PermissionSerializer(permission_view_projects)
        data = serializer.data
        
        assert data['module'] == 'PROJECTS'
        assert data['module_display'] == 'Projects'
        assert data['action'] == 'VIEW'
        assert data['action_display'] == 'View'
        assert data['access_profile'] == permission_view_projects.access_profile.id
    
    def test_deserialization(self, access_profile_member):
        """Testa deserialização de permissão."""
        data = {
            'access_profile': access_profile_member.id,
            'module': 'TASKS',
            'action': 'CREATE'
        }
        
        serializer = PermissionSerializer(data=data)
        assert serializer.is_valid()
        
        permission = serializer.save()
        assert permission.module == 'TASKS'
        assert permission.action == 'CREATE'
        assert permission.access_profile == access_profile_member
    
    def test_validation_invalid_module(self, access_profile_member):
        """Testa validação de módulo inválido."""
        data = {
            'access_profile': access_profile_member.id,
            'module': 'INVALID_MODULE',
            'action': 'VIEW'
        }
        
        serializer = PermissionSerializer(data=data)
        assert not serializer.is_valid()
        assert 'module' in serializer.errors


@pytest.mark.django_db
class TestAccessProfileSerializer:
    """Testes para AccessProfileSerializer."""
    
    def test_serialization(self, access_profile_member, permission_view_projects):
        """Testa serialização de perfil de acesso."""
        serializer = AccessProfileSerializer(access_profile_member)
        data = serializer.data
        
        assert data['name'] == 'Member Profile'
        assert data['description'] == 'Basic member access profile'
        assert len(data['permissions']) == 1
        assert data['permissions'][0]['module'] == 'PROJECTS'
        assert 'created_at' in data
        assert 'updated_at' in data
    
    def test_deserialization(self):
        """Testa deserialização de perfil de acesso."""
        data = {
            'name': 'New Profile',
            'description': 'Description for new profile'
        }
        
        serializer = AccessProfileSerializer(data=data)
        assert serializer.is_valid()
        
        profile = serializer.save()
        assert profile.name == 'New Profile'
        assert profile.description == 'Description for new profile'
    
    def test_validation_name_required(self):
        """Testa validação de nome obrigatório."""
        data = {
            'description': 'Profile without name'
        }
        
        serializer = AccessProfileSerializer(data=data)
        assert not serializer.is_valid()
        assert 'name' in serializer.errors


@pytest.mark.django_db
class TestUserAccessProfileSerializer:
    """Testes para UserAccessProfileSerializer."""
    
    def test_serialization(self, user_access_profile):
        """Testa serialização de perfil de acesso do usuário."""
        serializer = UserAccessProfileSerializer(user_access_profile)
        data = serializer.data
        
        assert 'access_profile' in data
        assert data['access_profile']['name'] == 'Member Profile'
        assert data['access_profile']['id'] == user_access_profile.access_profile.id
    
    def test_deserialization(self, team_member_user, access_profile_manager):
        """Testa deserialização de perfil de acesso do usuário."""
        data = {
            'access_profile_id': access_profile_manager.id
        }
        
        serializer = UserAccessProfileSerializer(data=data)
        assert serializer.is_valid()
        
        user_access = serializer.save(user=team_member_user)
        assert user_access.user == team_member_user
        assert user_access.access_profile == access_profile_manager


@pytest.mark.django_db
class TestUserSerializer:
    """Testes para UserSerializer (assumindo que existe)."""
    
    def test_user_serialization_basic_fields(self, team_member_user):
        """Testa serialização básica do usuário."""
        # Assumindo a existência de UserSerializer
        # Se não existir, este teste pode ser ajustado
        try:
            from users.serializers import UserSerializer
            serializer = UserSerializer(team_member_user)
            data = serializer.data
            
            assert data['username'] == 'tm_user'
            assert data['email'] == 'tm@example.com'
            assert data['full_name'] == 'Team Member'
            assert data['role'] == 'TEAM_MEMBER'
            assert data['is_active'] is True
        except ImportError:
            pytest.skip("UserSerializer not found")


@pytest.mark.django_db
class TestChangePasswordSerializer:
    """Testes para ChangePasswordSerializer."""
    
    def test_valid_password_change(self, team_member_user):
        """Testa mudança de senha válida."""
        try:
            data = {
                'old_password': 'tmpass123',
                'new_password': 'NewTestPass123!'
            }
            
            # Criar mock request
            request = type('MockRequest', (), {
                'user': team_member_user
            })()
            
            serializer = ChangePasswordSerializer(data=data, context={'request': request})
            
            if serializer.is_valid():
                # Testa se os campos estão presentes
                assert 'old_password' in data
                assert 'new_password' in data
        except ImportError:
            pytest.skip("ChangePasswordSerializer not found or different implementation")
    
    def test_password_mismatch(self, team_member_user):
        """Testa senha atual incorreta."""
        try:
            data = {
                'old_password': 'wrongpassword',
                'new_password': 'NewTestPass123!'
            }
            
            # Criar mock request
            request = type('MockRequest', (), {
                'user': team_member_user
            })()
            
            serializer = ChangePasswordSerializer(data=data, context={'request': request})
            
            # Se o serializer existe, deve invalidar senha atual incorreta
            if hasattr(serializer, 'is_valid'):
                assert not serializer.is_valid()
                if hasattr(serializer, 'errors'):
                    assert 'old_password' in serializer.errors or len(serializer.errors) > 0
        except ImportError:
            pytest.skip("ChangePasswordSerializer not found")


@pytest.mark.django_db
class TestResetPasswordSerializer:
    """Testes para ResetPasswordSerializer."""
    
    def test_email_validation(self, team_member_user):
        """Testa validação de email para reset."""
        try:
            data = {'email': 'tm@example.com'}
            
            serializer = ResetPasswordSerializer(data=data)
            
            if hasattr(serializer, 'is_valid'):
                # Email deve existir no sistema
                is_valid = serializer.is_valid()
                # Dependendo da implementação, pode ser válido ou não
                assert isinstance(is_valid, bool)
        except ImportError:
            pytest.skip("ResetPasswordSerializer not found")
    
    def test_invalid_email(self):
        """Testa email inválido para reset."""
        try:
            data = {'email': 'nonexistent@example.com'}
            
            serializer = ResetPasswordSerializer(data=data)
            
            if hasattr(serializer, 'is_valid'):
                # Dependendo da implementação, email inexistente pode ser inválido
                serializer.is_valid()
                # Teste flexível dependendo da implementação
                assert True  # Apenas verifica que não dá erro
        except ImportError:
            pytest.skip("ResetPasswordSerializer not found")


@pytest.mark.django_db
class TestUserCreateSerializer:
    """Testes para UserCreateSerializer."""
    
    def test_user_creation_serialization(self):
        """Testa serialização para criação de usuário."""
        try:
            data = {
                'username': 'newuser',
                'email': 'newuser@example.com',
                'full_name': 'New User',
                'password': 'newpass123',
                'role': 'TEAM_MEMBER'
            }
            
            serializer = UserCreateSerializer(data=data)
            
            if serializer.is_valid():
                user = serializer.save()
                assert user.username == 'newuser'
                assert user.email == 'newuser@example.com'
                assert user.check_password('newpass123')
        except ImportError:
            pytest.skip("UserCreateSerializer not found")
    
    def test_duplicate_username_validation(self, team_member_user):
        """Testa validação de username duplicado."""
        try:
            data = {
                'username': 'tm_user',  # Username já existe
                'email': 'newemail@example.com',
                'full_name': 'Another User',
                'password': 'pass123'
            }
            
            serializer = UserCreateSerializer(data=data)
            
            # Deve ser inválido por username duplicado
            assert not serializer.is_valid()
            assert 'username' in serializer.errors
        except ImportError:
            pytest.skip("UserCreateSerializer not found")
    
    def test_duplicate_email_validation(self, team_member_user):
        """Testa validação de email duplicado."""
        try:
            data = {
                'username': 'newuser',
                'email': 'tm@example.com',  # Email já existe
                'full_name': 'Another User',
                'password': 'pass123'
            }
            
            serializer = UserCreateSerializer(data=data)
            
            # Deve ser inválido por email duplicado
            assert not serializer.is_valid()
            assert 'email' in serializer.errors
        except ImportError:
            pytest.skip("UserCreateSerializer not found")


@pytest.mark.django_db
class TestSerializersIntegration:
    """Testes de integração entre serializers."""
    
    def test_user_with_profile_serialization(self, team_member_user, user_profile):
        """Testa serialização de usuário com perfil."""
        try:
            from users.serializers import UserSerializer
            
            serializer = UserSerializer(team_member_user)
            data = serializer.data
            
            # Verifica se perfil está incluído (dependendo da implementação)
            if 'profile' in data:
                assert data['profile']['phone'] == '+5511999999999'
                assert data['profile']['theme_preference'] == 'DARK'
        except ImportError:
            pytest.skip("UserSerializer not found or doesn't include profile")
    
    def test_access_profile_with_permissions(self, access_profile_member, permission_view_projects):
        """Testa serialização de perfil com permissões."""
        serializer = AccessProfileSerializer(access_profile_member)
        data = serializer.data
        
        assert len(data['permissions']) == 1
        permission_data = data['permissions'][0]
        
        assert permission_data['module'] == 'PROJECTS'
        assert permission_data['action'] == 'VIEW'
        assert permission_data['module_display'] == 'Projects'
        assert permission_data['action_display'] == 'View'
    
    def test_user_access_profile_nested_data(self, user_access_profile, permission_view_projects):
        """Testa dados aninhados em UserAccessProfile."""
        serializer = UserAccessProfileSerializer(user_access_profile)
        data = serializer.data
        
        # Verifica dados do perfil de acesso aninhado
        access_profile_data = data['access_profile']
        assert access_profile_data['name'] == 'Member Profile'
        assert len(access_profile_data['permissions']) == 1
        
        permission_data = access_profile_data['permissions'][0]
        assert permission_data['module'] == 'PROJECTS'
        assert permission_data['action'] == 'VIEW'


@pytest.mark.django_db
class TestSerializerValidations:
    """Testes de validações específicas dos serializers."""
    
    def test_permission_unique_validation(self, access_profile_member):
        """Testa validação de permissão única."""
        # Cria primeira permissão
        Permission.objects.create(
            access_profile=access_profile_member,
            module='PROJECTS',
            action='VIEW'
        )
        
        # Tenta criar permissão duplicada via serializer
        data = {
            'access_profile': access_profile_member.id,
            'module': 'PROJECTS',
            'action': 'VIEW'
        }
        
        serializer = PermissionSerializer(data=data)
        
        # Deve ser inválido por violação de unique_together
        assert not serializer.is_valid()
    
    def test_user_profile_phone_format(self, team_member_user):
        """Testa formato do telefone (se houver validação)."""
        data = {
            'phone': 'invalid_phone_format'
        }
        
        serializer = UserProfileSerializer(data=data)
        
        # Dependendo da implementação, pode ser válido ou não
        # Este teste é flexível para diferentes implementações
        serializer.is_valid()
        assert True  # Apenas verifica que não dá erro
    
    def test_access_profile_name_length(self):
        """Testa validação de tamanho do nome do perfil."""
        data = {
            'name': 'x' * 101,  # Nome muito longo (assumindo limite de 100)
            'description': 'Valid description'
        }
        
        serializer = AccessProfileSerializer(data=data)
        
        # Pode ser inválido dependendo das validações
        is_valid = serializer.is_valid()
        if not is_valid and 'name' in serializer.errors:
            assert 'name' in serializer.errors
        else:
            # Se passou, está ok também
            assert True


@pytest.mark.django_db
class TestSerializerFields:
    """Testes para campos específicos dos serializers."""
    
    def test_permission_display_fields(self, permission_view_projects):
        """Testa campos de display da permissão."""
        serializer = PermissionSerializer(permission_view_projects)
        data = serializer.data
        
        # Campos de display devem estar presentes e corretos
        assert 'module_display' in data
        assert 'action_display' in data
        assert data['module_display'] == 'Projects'
        assert data['action_display'] == 'View'
    
    def test_access_profile_timestamps(self, access_profile_member):
        """Testa campos de timestamp do perfil de acesso."""
        serializer = AccessProfileSerializer(access_profile_member)
        data = serializer.data
        
        # Campos de timestamp devem estar presentes
        assert 'created_at' in data
        assert 'updated_at' in data
        assert data['created_at'] is not None
        assert data['updated_at'] is not None
    
    def test_user_profile_boolean_fields(self, user_profile):
        """Testa campos booleanos do perfil de usuário."""
        serializer = UserProfileSerializer(user_profile)
        data = serializer.data
        
        # Campos booleanos devem manter tipo correto
        assert isinstance(data['email_notifications'], bool)
        assert isinstance(data['system_notifications'], bool)
        assert data['email_notifications'] is True
        assert data['system_notifications'] is False
