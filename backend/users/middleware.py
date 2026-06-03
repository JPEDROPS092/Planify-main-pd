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

        # R4: ativa o contexto de tenant da thread, deny-by-default. O TenantManager
        # consulta este contexto para filtrar toda query .objects de runtime. O
        # contexto é desativado em process_response/process_exception.
        from customers import context
        context.activate(tenant_id=None, bypass=False)

        # Verificar se é um caminho administrativo do Django
        if path.startswith('/admin/'):
            # Admin é ferramenta de staff/superuser: opera global (sem escopo de
            # tenant). Deixa o sistema de autenticação do admin do Django seguir.
            context.activate(tenant_id=None, bypass=True)
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

        # R3/R11: resolver o tenant da request a partir da TenantMembership ativa.
        # Superuser é administrador da plataforma, não owner implícito de tenant.
        self._set_request_tenant(request)
        
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

    def process_response(self, request, response):
        # R4: limpa o contexto de tenant da thread ao fim da request (evita que uma
        # thread reaproveitada carregue o tenant de uma request anterior).
        from customers import context
        context.deactivate()
        return response

    def process_exception(self, request, exception):
        from customers import context
        context.deactivate()
        return None

    def _set_request_tenant(self, request):
        """Resolve e fixa o tenant da request (R3).

        Seta ``request.tenant`` (o ``Client`` ou ``None``), ``request.tenant_id``
        e ``request._tenant_membership`` (cache para o RLS/permissões). Atualiza
        também o contexto de tenant da thread (R4) que dirige o ``TenantManager``.
        """
        from customers import context
        from customers.tenancy import resolve_request_tenant

        tenant, membership = resolve_request_tenant(request)
        request.tenant = tenant
        request.tenant_id = tenant.id if tenant is not None else None
        request._tenant_membership = membership

        # Sem tenant resolvido, tenant_id=None -> manager devolve none().
        context.activate(tenant_id=request.tenant_id, bypass=False)

    def check_tenant_membership(self, request):
        protected_prefixes = getattr(settings, 'TENANT_MEMBERSHIP_REQUIRED_PATH_PREFIXES', ())
        if not request.path_info.startswith(protected_prefixes):
            return None

        # Fonte única de verdade do vínculo "(user, tenant) ativo", compartilhada
        # com a permissão DRF IsTenantMember e o RLS (usa request._tenant_membership
        # já resolvido em _set_request_tenant). Sem tenant resolvido → sem vínculo.
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
