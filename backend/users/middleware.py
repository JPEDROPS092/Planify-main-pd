import re
import logging
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .permissions import get_required_permission, check_user_permission, log_unauthorized_access, PUBLIC_PATHS
from users.models import AccessAttempt

logger = logging.getLogger(__name__)

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
        
        # Administradores têm acesso total
        if user.is_superuser or user.role == 'ADMIN':
            return None
        
        # Verificar se a conta está bloqueada
        if hasattr(user, 'is_locked') and user.is_locked:
            return JsonResponse({"detail": "Conta bloqueada. Entre em contato com o administrador."}, status=403)
        
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

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
