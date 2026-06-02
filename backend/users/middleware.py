import re
import logging
from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .permissions import get_required_permission, check_user_permission, log_unauthorized_access, PUBLIC_PATHS
from users.models import AccessAttempt

logger = logging.getLogger(__name__)

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
TENANT_ROLE_METHOD_RULES = {
    'owner': {'*': ('*',)},
    'admin': {'*': ('*',)},
    'manager': {'*': ('*',)},
    'member': {
        '/api/tasks/': SAFE_METHODS + ('POST', 'PUT', 'PATCH'),
        '/api/documents/': SAFE_METHODS + ('POST', 'PUT', 'PATCH'),
        '/api/communications/': SAFE_METHODS + ('POST', 'PUT', 'PATCH'),
    },
    'viewer': {'*': SAFE_METHODS},
}

class PermissionMiddleware(MiddlewareMixin):
    """Middleware para verificar permissões de acesso."""
    
    def __init__(self, get_response):
        super().__init__(get_response)
        self.jwt_auth = JWTAuthentication()

    def process_request(self, request):
        # Obter o caminho da requisição
        path = request.path_info
        
        # Verificar se é um caminho administrativo do Django
        if path.startswith('/admin/'):
            # Deixa o sistema de autenticação do admin do Django lidar com isso
            return None
        
        # Verificar se é um caminho público
        for pattern in PUBLIC_PATHS:
            if re.match(pattern, path):
                return None
        
        # Verificar o token JWT
        try:
            header = request.headers.get('Authorization', '')
            if not header.startswith('Bearer '):
                return JsonResponse(
                    {"detail": "Autenticação JWT é necessária para acessar este recurso."},
                    status=401
                )
                
            token = header.split(' ')[1]
            validated_token = self.jwt_auth.get_validated_token(token)
            request.user = self.jwt_auth.get_user(validated_token)
            
        except (InvalidToken, TokenError):
            return JsonResponse(
                {"detail": "Token inválido ou expirado."},
                status=401
            )
        except Exception as e:
            return JsonResponse(
                {"detail": str(e)},
                status=401
            )

        # Verificar se o usuário está autenticado
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"detail": "Autenticação necessária"}, status=401)
        
        if user.is_superuser:
            return None
        
        # Verificar se a conta está bloqueada
        if hasattr(user, 'is_locked') and user.is_locked:
            return JsonResponse({"detail": "Conta bloqueada. Entre em contato com o administrador."}, status=403)

        tenant_response = self.check_tenant_membership(request)
        if tenant_response is not None:
            return tenant_response
        
        # Obter permissão necessária para o caminho
        permission = get_required_permission(path)
        
        # Se não for necessária permissão específica, permitir acesso
        if not permission:
            return None
        
        module, action = permission
        
        # Verificar se o usuário tem permissão
        if not check_user_permission(user, module, action):
            # Registrar tentativa de acesso não autorizado
            log_unauthorized_access(user, path, module, action)
            
            # Obter o IP do cliente
            client_ip = self.get_client_ip(request)

            # Registrar a tentativa no banco de dados
            AccessAttempt.objects.create(
                user=request.user,
                endpoint=request.path,
                method=request.method,
                ip_address=client_ip,
                timestamp=timezone.now(),
                success=False
            )

            # Retornar erro de permissão negada
            logger.warning(f"Usuário {request.user.username} não tem permissão {module}.{action} para acessar {request.path} (IP: {client_ip})")
            return JsonResponse({
                'error': 'Forbidden',
                'message': 'You do not have permission to access this resource'
            }, status=403)
        
        return None

    def check_tenant_membership(self, request):
        tenant = getattr(request, 'tenant', None)
        schema_name = getattr(tenant, 'schema_name', settings.PUBLIC_SCHEMA_NAME)

        if schema_name == settings.PUBLIC_SCHEMA_NAME:
            return None

        protected_prefixes = getattr(settings, 'TENANT_MEMBERSHIP_REQUIRED_PATH_PREFIXES', ())
        if not request.path_info.startswith(protected_prefixes):
            return None

        # Mesma resolução de vínculo usada pela permissão DRF IsTenantMember
        # e pelo RLS (customers.querysets.get_request_membership), mantendo
        # uma única fonte de verdade para "vínculo ativo em (user, tenant)".
        from customers.querysets import get_request_membership

        membership = get_request_membership(request)

        if not membership:
            return JsonResponse({
                'error': 'Forbidden',
                'message': 'Usuário não possui acesso a este tenant.'
            }, status=403)

        if self.is_tenant_role_allowed(membership.role, request.path_info, request.method):
            return None

        return JsonResponse({
            'error': 'Forbidden',
            'message': 'Papel do usuário não permite esta ação neste tenant.'
        }, status=403)

    def is_tenant_role_allowed(self, role, path, method):
        rules = TENANT_ROLE_METHOD_RULES.get(role, {})
        allowed_methods = rules.get('*')

        for prefix, methods in rules.items():
            if prefix == '*':
                continue
            if path.startswith(prefix):
                allowed_methods = methods
                break

        if not allowed_methods:
            allowed_methods = SAFE_METHODS

        return '*' in allowed_methods or method in allowed_methods

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
