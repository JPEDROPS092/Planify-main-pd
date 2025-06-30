# users/validators.py
import re
from django.core.exceptions import ValidationError
# from django.contrib.auth.password_validation import validate_password # Removido, pois não é usado diretamente aqui
# from django.contrib.auth import get_user_model # Removido, pois não é usado diretamente aqui
import logging

logger = logging.getLogger(__name__)


class PasswordPolicyValidator:
    """
    Validador de política de senhas personalizado.
    Inclui verificação de histórico de senhas.
    """

    def __init__(self, min_length=8, require_uppercase=True,
                 require_lowercase=True, require_numbers=True,
                 require_special=True, max_length=128,
                 password_history_count=5): # Novo parâmetro para o histórico
        self.min_length = min_length
        self.max_length = max_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_numbers = require_numbers
        self.require_special = require_special
        self.password_history_count = password_history_count # Armazena a contagem do histórico

    def validate(self, password, user=None):
        """
        Valida a senha conforme as políticas definidas.
        """
        errors = []

        # --- Validações de política de senha ---
        if len(password) < self.min_length:
            errors.append(f'A senha deve ter pelo menos {self.min_length} caracteres.')
        if len(password) > self.max_length:
            errors.append(f'A senha deve ter no máximo {self.max_length} caracteres.')
        if self.require_uppercase and not re.search(r'[A-Z]', password):
            errors.append('A senha deve conter pelo menos uma letra maiúscula.')
        if self.require_lowercase and not re.search(r'[a-z]', password):
            errors.append('A senha deve conter pelo menos uma letra minúscula.')
        if self.require_numbers and not re.search(r'\d', password):
            errors.append('A senha deve conter pelo menos um número.')
        if self.require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append('A senha deve conter pelo menos um caractere especial (!@#$%^&*(),.?":{}|<>).')
        if self._is_common_password(password):
            errors.append('Esta senha é muito comum. Escolha uma senha mais segura.')
        if user and self._contains_user_info(password, user):
            errors.append('A senha não pode conter informações pessoais como nome de usuário ou email.')

        # --- Validação de histórico de senhas ---
        if user and self.password_history_count > 0: # Só verifica se o usuário existe e a contagem é > 0
            try:
                self._validate_password_history(user, password)
            except ValidationError as e:
                errors.extend(e.messages) # Adiciona mensagens de erro do histórico

        if errors:
            raise ValidationError(errors)

    def _is_common_password(self, password):
        """
        Verifica se a senha está na lista de senhas comuns.
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
        Verifica se a senha contém informações do usuário.
        """
        if not user: # Esta verificação já existe no método validate
            return False

        user_info = []
        if hasattr(user, 'username') and user.username:
            user_info.append(user.username.lower())
        if hasattr(user, 'email') and user.email:
            email_local = user.email.split('@')[0].lower()
            user_info.append(email_local)
        if hasattr(user, 'full_name') and user.full_name:
            name_parts = user.full_name.lower().split()
            user_info.extend(name_parts)

        password_lower = password.lower()
        for info in user_info:
            if len(info) >= 3 and info in password_lower:
                return True
        return False

    def _validate_password_history(self, user, new_password):
        """
        Verifica se a nova senha não foi usada recentemente.
        Este é um método auxiliar chamado por `validate`.
        """
        # A verificação 'if not user or not hasattr(user, 'pk') or not user.pk:'
        # é feita antes de chamar este método, em `validate`.
        try:
            from .models import PasswordHistory # Importação local

            recent_passwords_qs = PasswordHistory.objects.filter(
                user=user
            ).order_by('-created_at')[:self.password_history_count]

            for password_entry in recent_passwords_qs:
                if user.check_password(new_password, password_entry.password_hash):
                    raise ValidationError(
                        "Você não pode reutilizar uma senha recente. Por favor, escolha uma senha diferente.",
                        code='password_reused'
                    )
        except ImportError:
            logger.warning(
                "O modelo PasswordHistory não foi encontrado. "
                "A verificação do histórico de senhas foi pulada."
            )
        except Exception as e:
            logger.error(
                f"Erro inesperado ao verificar histórico de senhas para o usuário {user.username}: {str(e)}"
            )
            # Considerar se deve levantar um ValidationError genérico aqui
            # para falhar seguro, ou deixar passar (como está agora, apenas logando).
            # Para segurança, é melhor falhar:
            # raise ValidationError("Não foi possível verificar o histórico de senhas. Tente novamente.", code='history_check_failed')


    def get_help_text(self):
        """
        Retorna texto de ajuda para o usuário.
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
        if self.password_history_count > 0:
            requirements.append(f'Não pode ser igual a nenhuma das suas últimas {self.password_history_count} senhas.')

        return ' '.join(requirements)


def validate_username(username):
    """
    Valida o nome de usuário.
    """
    if not username:
        raise ValidationError('Nome de usuário é obrigatório.')
    if len(username) < 3:
        raise ValidationError('Nome de usuário deve ter pelo menos 3 caracteres.')
    if len(username) > 30:
        raise ValidationError('Nome de usuário deve ter no máximo 30 caracteres.')
    if not re.match(r'^[a-zA-Z0-9._-]+$', username):
        raise ValidationError('Nome de usuário pode conter apenas letras, números, pontos, hífens e sublinhados.')
    if username[0] in '._-' or username[-1] in '._-':
        raise ValidationError('Nome de usuário não pode começar ou terminar com caracteres especiais.')
    reserved_usernames = [
        'admin', 'administrator', 'root', 'api', 'www', 'ftp', 'mail',
        'email', 'support', 'help', 'info', 'contact', 'about', 'test',
        'demo', 'guest', 'user', 'null', 'undefined', 'system'
    ]
    if username.lower() in reserved_usernames:
        raise ValidationError('Este nome de usuário é reservado e não pode ser usado.')


def validate_full_name(full_name):
    """
    Valida o nome completo.
    """
    if not full_name:
        raise ValidationError('Nome completo é obrigatório.')
    if len(full_name.strip()) < 2: # strip() para remover espaços nas pontas antes de checar tamanho
        raise ValidationError('Nome completo deve ter pelo menos 2 caracteres.')
    if len(full_name) > 100:
        raise ValidationError('Nome completo deve ter no máximo 100 caracteres.')
    if not re.match(r'^[a-zA-ZÀ-ÿ\s\'\-\.]+$', full_name):
        raise ValidationError('Nome completo pode conter apenas letras, espaços, acentos, apostrofes, hífens e pontos.')
