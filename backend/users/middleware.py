# users/middleware.py - Melhorias
from django.contrib.auth import logout
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger('security')

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar tentativas de login
        if request.user.is_authenticated:
            self._check_account_security(request)
            self._check_password_expiry(request)
            self._log_suspicious_activity(request)
        
        response = self.get_response(request)
        return response

    def _check_account_security(self, request):
        user = request.user
        
        # Verificar se conta está bloqueada
        if user.locked_until and user.locked_until > timezone.now():
            logout(request)
            return
            
        # Verificar força de alteração de senha
        if user.force_password_change:
            # Redirecionar para alteração de senha
            pass

    def _check_password_expiry(self, request):
        user = request.user
        password_max_age = timedelta(days=90)  # Configurável
        
        if user.last_password_change:
            if timezone.now() - user.last_password_change > password_max_age:
                user.force_password_change = True
                user.save()

    def _log_suspicious_activity(self, request):
        # Detectar atividades suspeitas
        # Múltiplos IPs, horários incomuns, etc.
        pass


class PermissionMiddleware:
    """Middleware para verificação de permissões centralizadas"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response