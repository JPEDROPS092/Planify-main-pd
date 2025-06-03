"""
Utilitários para o módulo de usuários.
Contém funções auxiliares para gerenciamento de usuários, senhas e permissões.
"""
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

def update_user_password(user, new_password):
    """
    Atualiza a senha do usuário e registra a alteração.
    
    Args:
        user: Instância do modelo User
        new_password: Nova senha a ser definida
        
    Returns:
        user: Usuário atualizado
    """
    user.set_password(new_password)
    
    # Atualizar campos relacionados à senha
    if hasattr(user, 'password_change_required'):
        user.password_change_required = False
    
    if hasattr(user, 'last_password_change'):
        user.last_password_change = timezone.now()
    
    user.save()
    logger.info(f"Senha alterada para o usuário: {user.username} (ID: {user.id})")
    
    return user

def check_user_permission(user, module, action):
    """
    Verifica se um usuário tem permissão para uma ação específica em um módulo.
    
    Args:
        user: Instância do modelo User
        module: Módulo a ser verificado (ex: 'PROJECTS', 'TASKS')
        action: Ação a ser verificada (ex: 'VIEW', 'CREATE', 'EDIT', 'DELETE')
        
    Returns:
        bool: True se o usuário tem permissão, False caso contrário
    """
    # Administradores têm acesso total
    if user.is_superuser or user.role == 'ADMIN':
        return True
    
    # Verificar permissão específica
    return user.has_permission(module, action)

def create_user_with_profile(validated_data):
    """
    Cria um usuário com seu perfil associado.
    
    Args:
        validated_data: Dados validados do serializer
        
    Returns:
        user: Usuário criado
    """
    from django.contrib.auth import get_user_model
    from .models import UserProfile
    
    User = get_user_model()
    
    # Extrair dados do perfil se fornecidos
    profile_data = validated_data.pop('profile', None)
    password = validated_data.pop('password', None)
    
    # Definir o papel padrão como TEAM_MEMBER se não for especificado
    if 'role' not in validated_data:
        validated_data['role'] = 'TEAM_MEMBER'
    
    # Criar o usuário
    user = User.objects.create(**validated_data)
    
    # Definir senha se fornecida
    if password:
        user.set_password(password)
        user.save()
    
    # Criar perfil do usuário
    if profile_data:
        UserProfile.objects.create(user=user, **profile_data)
    else:
        UserProfile.objects.create(user=user)
    
    logger.info(f"Usuário criado: {user.username} (ID: {user.id})")
    return user
