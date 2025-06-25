"""
Utility functions para o app users.
Versão simplificada mantendo apenas funções essenciais.
"""

import logging
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction

User = get_user_model()
logger = logging.getLogger(__name__)


def update_user_password(user, new_password):
    """
    Atualiza a senha do usuário de forma segura.
    
    Args:
        user: Instância do usuário
        new_password: Nova senha em texto plano
    
    Returns:
        bool: True se a senha foi atualizada com sucesso
        
    Raises:
        ValidationError: Se os dados não são válidos
    """
    if not user:
        raise ValidationError("Usuário não pode ser None")
    
    if not new_password:
        raise ValidationError("Senha não pode ser vazia")
    
    try:
        with transaction.atomic():
            # Validar a nova senha
            from django.contrib.auth.password_validation import validate_password
            validate_password(new_password, user)
            
            # Atualizar a senha
            user.set_password(new_password)
            user.save()
            
            logger.info(f"Senha atualizada para usuário {user.username}")
            return True
            
    except Exception as e:
        logger.error(f"Erro ao atualizar senha do usuário {user.username}: {str(e)}")
        raise


def create_user_with_profile(validated_data):
    """
    Cria um usuário e seu perfil associado.
    
    Args:
        validated_data: Dados validados do serializer
        
    Returns:
        User: Instância do usuário criado
    """
    try:
        with transaction.atomic():
            # Extrair dados específicos do perfil se existirem
            profile_data = {}
            
            # Criar o usuário usando o manager customizado
            user = User(**validated_data)
            if 'password' in validated_data:
                user.set_password(validated_data['password'])
            user.save()
            
            # Criar perfil se o modelo UserProfile existir
            try:
                from .models import UserProfile
                UserProfile.objects.get_or_create(
                    user=user,
                    defaults=profile_data
                )
            except ImportError:
                # UserProfile não existe, pular criação
                pass
            
            logger.info(f"Usuário criado com sucesso: {user.pk}")
            return user
            
    except Exception as e:
        logger.error(f"Erro ao criar usuário: {str(e)}")
        raise
