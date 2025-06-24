"""
Utilitários para o módulo de usuários.
Contém funções auxiliares para gerenciamento de usuários, senhas e permissões.
"""
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
import logging
import secrets
import string

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """
    Obtém o IP real do cliente, considerando proxies
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    """
    Obtém o user agent do request
    """
    return request.META.get('HTTP_USER_AGENT', '')


def generate_secure_password(length=12):
    """
    Gera uma senha segura aleatória
    """
    # Definir caracteres permitidos
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase  
    digits = string.digits
    special = '!@#$%^&*(),.?":{}|<>'
    
    # Garantir pelo menos um de cada tipo
    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(special)
    ]
    
    # Preencher o resto com caracteres aleatórios
    all_chars = lowercase + uppercase + digits + special
    for _ in range(length - 4):
        password.append(secrets.choice(all_chars))
    
    # Embaralhar a senha
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)


def update_user_password(user, new_password):
    """
    Atualiza a senha do usuário e registra a alteração.
    
    Args:
        user: Instância do modelo User
        new_password: Nova senha a ser definida
        
    Returns:
        user: Usuário atualizado
    """
    if not user:
        raise ValueError("Usuário é obrigatório")
    if not new_password:
        raise ValueError("Nova senha é obrigatória")
    
    try:
        # Salvar senha anterior no histórico se o modelo existir
        try:
            from .models import PasswordHistory
            if user.pk and user.password:  # Usuário existente com senha
                PasswordHistory.objects.create(
                    user=user,
                    password_hash=user.password
                )
                
                # Manter apenas os últimos 5 registros
                old_passwords = PasswordHistory.objects.filter(user=user).order_by('-created_at')[5:]
                if old_passwords:
                    old_password_ids = [p.pk for p in old_passwords]
                    PasswordHistory.objects.filter(
                        pk__in=old_password_ids
                    ).delete()
                    
        except ImportError:
            logger.info("Modelo PasswordHistory não encontrado, pulando histórico")
        except Exception as e:
            logger.warning(f"Erro ao salvar histórico de senha: {str(e)}")
        
        # Definir nova senha
        user.set_password(new_password)
        
        # Atualizar campos relacionados à senha
        if hasattr(user, 'password_change_required'):
            user.password_change_required = False
        
        if hasattr(user, 'last_password_change'):
            user.last_password_change = timezone.now()
            
        if hasattr(user, 'force_password_change'):
            user.force_password_change = False
        
        user.save()
        logger.info(f"Senha alterada para o usuário: {user.username} (ID: {user.id})")
        
        # Enviar notificação de segurança
        try:
            from .security_notifications import SecurityNotificationService
            SecurityNotificationService.notify_password_change(user)
        except Exception as e:
            logger.warning(f"Erro ao enviar notificação de alteração de senha: {str(e)}")
        
        return user
        
    except Exception as e:
        logger.error(f"Erro ao atualizar senha do usuário {user.username}: {str(e)}")
        raise


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
    try:
        # Administradores têm acesso total
        if user.is_superuser or user.role == 'ADMIN':
            return True
        
        # Verificar permissão específica
        return user.has_permission(module, action)
        
    except Exception as e:
        logger.warning(f"Erro ao verificar permissão para usuário {user.username}: {str(e)}")
        return False


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
    
    try:
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
            if hasattr(user, 'last_password_change'):
                user.last_password_change = timezone.now()
            user.save()
        
        # Criar perfil do usuário
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        else:
            UserProfile.objects.create(user=user)
        
        logger.info(f"Usuário criado: {getattr(user, 'username', 'N/A')} (ID: {getattr(user, 'id', 'N/A')})")
        
        # Criar log de auditoria
        try:
            from .audit import create_audit_log
            user_role = getattr(user, 'role', 'UNKNOWN')
            create_audit_log(
                user=user,
                action='USER_CREATED',
                details={'role': user_role}
            )
        except Exception as e:
            logger.warning(f"Erro ao criar log de auditoria: {str(e)}")
        
        return user
        
    except Exception as e:
        logger.error(f"Erro ao criar usuário: {str(e)}")
        raise


def lock_user_account(user, reason='Múltiplas tentativas de login falhadas'):
    """
    Bloqueia a conta do usuário
    """
    if not user:
        raise ValueError("Usuário é obrigatório")
    
    try:
        user.is_locked = True
        user.locked_until = timezone.now() + timedelta(minutes=30)  # Bloquear por 30 minutos
        user.save(update_fields=['is_locked', 'locked_until'])
        
        logger.warning(f"Conta bloqueada para usuário {user.username}: {reason}")
        
        # Criar log de auditoria
        try:
            from .audit import create_audit_log
            create_audit_log(
                user=user,
                action='ACCOUNT_LOCKED',
                details={'reason': reason}
            )
        except Exception as e:
            logger.warning(f"Erro ao criar log de auditoria: {str(e)}")
        
        # Enviar notificação
        try:
            from .security_notifications import SecurityNotificationService
            SecurityNotificationService.notify_account_locked(user, reason)
        except Exception as e:
            logger.warning(f"Erro ao enviar notificação de bloqueio: {str(e)}")
            
    except Exception as e:
        logger.error(f"Erro ao bloquear conta do usuário {user.username}: {str(e)}")


def unlock_user_account(user):
    """
    Desbloqueia a conta do usuário
    """
    if not user:
        raise ValueError("Usuário é obrigatório")
    
    try:
        user.is_locked = False
        user.locked_until = None
        user.failed_login_attempts = 0
        user.save(update_fields=['is_locked', 'locked_until', 'failed_login_attempts'])
        
        logger.info(f"Conta desbloqueada para usuário {user.username}")
        
        # Criar log de auditoria
        try:
            from .audit import create_audit_log
            create_audit_log(
                user=user,
                action='ACCOUNT_UNLOCKED'
            )
        except Exception as e:
            logger.warning(f"Erro ao criar log de auditoria: {str(e)}")
        
        # Enviar notificação
        try:
            from .security_notifications import SecurityNotificationService
            SecurityNotificationService.notify_account_unlocked(user)
        except Exception as e:
            logger.warning(f"Erro ao enviar notificação de desbloqueio: {str(e)}")
            
    except Exception as e:
        logger.error(f"Erro ao desbloquear conta do usuário {user.username}: {str(e)}")


def is_account_locked(user):
    """
    Verifica se a conta do usuário está bloqueada
    """
    if not user:
        return False
    
    if not hasattr(user, 'is_locked') or not user.is_locked:
        return False
    
    # Verificar se o bloqueio temporário expirou
    if hasattr(user, 'locked_until') and user.locked_until:
        if timezone.now() > user.locked_until:
            # Desbloqueio automático
            unlock_user_account(user)
            return False
    
    return True


def clean_expired_tokens():
    """
    Remove tokens expirados da blacklist
    """
    try:
        from .models import BlacklistedTokens
        from django.utils import timezone
        from datetime import timedelta
        
        # Remove tokens com mais de 7 dias
        cutoff_date = timezone.now() - timedelta(days=7)
        expired_count = BlacklistedTokens.objects.filter(
            created_at__lt=cutoff_date
        ).count()
        
        BlacklistedTokens.objects.filter(
            created_at__lt=cutoff_date
        ).delete()
        
        logger.info(f"Removidos {expired_count} tokens expirados da blacklist")
        
    except Exception as e:
        logger.error(f"Erro ao limpar tokens expirados: {str(e)}")


def send_password_reset_email(user, reset_link):
    """
    Envia email de reset de senha
    """
    if not user or not user.email:
        raise ValueError("Usuário com email válido é obrigatório")
    if not reset_link:
        raise ValueError("Link de reset é obrigatório")
    
    try:
        subject = 'Redefinição de Senha - Planify'
        html_message = f"""
        <html>
        <body>
            <h2>Redefinição de Senha</h2>
            <p>Olá {user.full_name or user.username},</p>
            
            <p>Você solicitou a redefinição de sua senha.</p>
            
            <p>Clique no link abaixo para redefinir sua senha:</p>
            <p><a href="{reset_link}">Redefinir Senha</a></p>
            
            <p>Este link expira em 24 horas.</p>
            
            <p>Se você não solicitou esta redefinição, ignore este email.</p>
            
            <p>Atenciosamente,<br>Equipe Planify</p>
        </body>
        </html>
        """
        
        from django.utils.html import strip_tags
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@planify.com'),
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        logger.info(f"Email de reset de senha enviado para {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao enviar email de reset de senha: {str(e)}")
        return False
