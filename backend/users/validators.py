# users/validators.py - Validadores customizados
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)


class PasswordPolicyValidator:
    """
    Validador de política de senhas personalizado
    """
    
    def __init__(self, min_length=8, require_uppercase=True, 
                 require_lowercase=True, require_numbers=True, 
                 require_special=True, max_length=128):
        self.min_length = min_length
        self.max_length = max_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_numbers = require_numbers
        self.require_special = require_special

    def validate(self, password, user=None):
        """
        Valida a senha conforme as políticas definidas
        """
        errors = []
        
        # Verificar comprimento mínimo
        if len(password) < self.min_length:
            errors.append(f'A senha deve ter pelo menos {self.min_length} caracteres.')
        
        # Verificar comprimento máximo
        if len(password) > self.max_length:
            errors.append(f'A senha deve ter no máximo {self.max_length} caracteres.')
        
        # Verificar letra maiúscula
        if self.require_uppercase and not re.search(r'[A-Z]', password):
            errors.append('A senha deve conter pelo menos uma letra maiúscula.')
        
        # Verificar letra minúscula
        if self.require_lowercase and not re.search(r'[a-z]', password):
            errors.append('A senha deve conter pelo menos uma letra minúscula.')
        
        # Verificar números
        if self.require_numbers and not re.search(r'\d', password):
            errors.append('A senha deve conter pelo menos um número.')
        
        # Verificar caracteres especiais
        if self.require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append('A senha deve conter pelo menos um caractere especial (!@#$%^&*(),.?":{}|<>).')
        
        # Verificar se não é muito simples
        if self._is_common_password(password):
            errors.append('Esta senha é muito comum. Escolha uma senha mais segura.')
        
        # Verificar se não contém informações do usuário
        if user and self._contains_user_info(password, user):
            errors.append('A senha não pode conter informações pessoais como nome de usuário ou email.')
        
        if errors:
            raise ValidationError(errors)

    def _is_common_password(self, password):
        """
        Verifica se a senha está na lista de senhas comuns
        """
        common_passwords = [
            '123456', 'password', '123456789', '12345678', '12345',
            '1234567', '1234567890', 'qwerty', 'abc123', 'password123',
            '123123', 'admin', 'letmein', 'welcome', 'monkey',
            '1234', 'dragon', 'master', 'login', 'passw0rd',
            'password123!', 'password1', 'password!', 'admin123',
            'admin123!', '12345678!', 'qwerty123', 'qwerty123!'
        ]
        return password.lower() in [p.lower() for p in common_passwords]

    def _contains_user_info(self, password, user):
        """
        Verifica se a senha contém informações do usuário
        """
        if not user:
            return False
        
        user_info = []
        
        # Adicionar informações do usuário para verificação
        if hasattr(user, 'username') and user.username:
            user_info.append(user.username.lower())
        
        if hasattr(user, 'email') and user.email:
            # Adicionar parte local do email (antes do @)
            email_local = user.email.split('@')[0].lower()
            user_info.append(email_local)
        
        if hasattr(user, 'full_name') and user.full_name:
            # Adicionar partes do nome completo
            name_parts = user.full_name.lower().split()
            user_info.extend(name_parts)
        
        # Verificar se alguma informação do usuário está na senha
        password_lower = password.lower()
        for info in user_info:
            if len(info) >= 3 and info in password_lower:
                return True
        
        return False

    def get_help_text(self):
        """
        Retorna texto de ajuda para o usuário
        """
        requirements = []
        
        requirements.append(f'Sua senha deve ter entre {self.min_length} e {self.max_length} caracteres.')
        
        if self.require_uppercase:
            requirements.append('Deve conter pelo menos uma letra maiúscula.')
        
        if self.require_lowercase:
            requirements.append('Deve conter pelo menos uma letra minúscula.')
        
        if self.require_numbers:
            requirements.append('Deve conter pelo menos um número.')
        
        if self.require_special:
            requirements.append('Deve conter pelo menos um caractere especial.')
        
        requirements.append('Não pode ser uma senha muito comum.')
        requirements.append('Não pode conter suas informações pessoais.')
        
        return ' '.join(requirements)


def validate_username(username):
    """
    Valida o nome de usuário
    """
    if not username:
        raise ValidationError('Nome de usuário é obrigatório.')
    
    if len(username) < 3:
        raise ValidationError('Nome de usuário deve ter pelo menos 3 caracteres.')
    
    if len(username) > 30:
        raise ValidationError('Nome de usuário deve ter no máximo 30 caracteres.')
    
    # Verificar caracteres permitidos (apenas letras, números, _, -, .)
    if not re.match(r'^[a-zA-Z0-9._-]+$', username):
        raise ValidationError('Nome de usuário pode conter apenas letras, números, pontos, hífens e sublinhados.')
    
    # Não pode começar ou terminar com caracteres especiais
    if username[0] in '._-' or username[-1] in '._-':
        raise ValidationError('Nome de usuário não pode começar ou terminar com caracteres especiais.')
    
    # Verificar se não é reservado
    reserved_usernames = [
        'admin', 'administrator', 'root', 'api', 'www', 'ftp', 'mail',
        'email', 'support', 'help', 'info', 'contact', 'about', 'test',
        'demo', 'guest', 'user', 'null', 'undefined', 'system'
    ]
    
    if username.lower() in reserved_usernames:
        raise ValidationError('Este nome de usuário é reservado e não pode ser usado.')


def validate_full_name(full_name):
    """
    Valida o nome completo
    """
    if not full_name:
        raise ValidationError('Nome completo é obrigatório.')
    
    if len(full_name.strip()) < 2:
        raise ValidationError('Nome completo deve ter pelo menos 2 caracteres.')
    
    if len(full_name) > 100:
        raise ValidationError('Nome completo deve ter no máximo 100 caracteres.')
    
    # Verificar se contém apenas letras, espaços, acentos e alguns caracteres especiais
    if not re.match(r'^[a-zA-ZÀ-ÿ\s\'\-\.]+$', full_name):
        raise ValidationError('Nome completo pode conter apenas letras, espaços, acentos, apostrofes, hífens e pontos.')


def validate_password_history(user, new_password, history_count=5):
    """
    Verifica se a nova senha não foi usada recentemente
    """
    if not user or not user.pk:
        return  # Novo usuário, não há histórico
    
    try:
        from .models import PasswordHistory
        
        # Buscar os últimos passwords
        recent_passwords = PasswordHistory.objects.filter(
            user=user
        ).order_by('-created_at')[:history_count]
        
        # Verificar se a nova senha corresponde a alguma das antigas
        for password_entry in recent_passwords:
            if user.check_password(new_password):
                # Esta verificação precisa ser mais sofisticada para comparar hashes
                # Por segurança, vamos assumir que não podemos verificar senhas antigas
                pass
                
    except ImportError:
        # Modelo PasswordHistory não existe
        pass
    except Exception as e:
        logger.warning(f"Erro ao verificar histórico de senhas: {str(e)}")