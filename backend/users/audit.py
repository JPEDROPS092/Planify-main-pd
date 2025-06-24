# users/audit.py - Sistema de auditoria
from django.utils import timezone
from .models import AuditLog


def log_user_action(user, action, ip_address=None, user_agent=None, details=None):
    """
    Registra uma ação do usuário no sistema de auditoria
    
    Args:
        user: Instância do modelo User
        action: String com a ação realizada (deve estar em ACTION_CHOICES)
        ip_address: IP do usuário (opcional)
        user_agent: User agent do browser (opcional)
        details: Dicionário com detalhes adicionais (opcional)
    """
    if details is None:
        details = {}
    
    AuditLog.objects.create(
        user=user,
        action=action,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details
    )


def create_audit_log(user, action, ip_address=None, user_agent=None, details=None, content_object=None):
    """
    Função utilitária para criar logs de auditoria
    """
    audit_data = {
        'user': user,
        'action': action,
        'ip_address': ip_address,
        'user_agent': user_agent or '',
        'details': details or {},
    }
    
    if content_object:
        audit_data['content_object'] = content_object
    
    return AuditLog.objects.create(**audit_data)