import re
import logging
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .permissions import get_required_permission, check_user_permission, log_unauthorized_access, PUBLIC_PATHS
from users.models import AccessAttempt, BlacklistedTokens

logger = logging.getLogger(__name__)

class PermissionMiddleware(MiddlewareMixin):
    """Middleware para verificar permissões de acesso."""
    
    def __init__(self, get_response):
        super().__init__(get_response)
        self.jwt_auth = JWTAuthentication()

    def process_request(self, request):
        # Obter o caminho da requisição
        path = request.path_info
        logger.debug(f"Processing request for path: {path}")
        
        # Primeiro verificar se é um caminho público
        for pattern in PUBLIC_PATHS:
            if re.match(pattern, path):
                logger.debug(f"Path {path} matches public pattern {pattern}")
                return None
                
        # Em seguida verificar se é um caminho administrativo do Django
        if path.startswith('/admin/'):
            logger.debug(f"Path {path} is an admin path")
            return None
        
        # Se não for público nem admin, verificar o token JWT
        try:
            header = request.headers.get('Authorization', '')
            # Se não tiver token em um caminho protegido
            if not header:
                logger.debug(f"No Authorization header present for protected path {path}")
                return JsonResponse(
                    {"detail": "Autenticação é necessária para acessar este recurso."},
                    status=401
                )
            
            # Verificar formato do header (aceitar tanto Bearer quanto JWT)
            header_parts = header.split()
            if len(header_parts) != 2 or header_parts[0] not in ('Bearer', 'JWT'):
                logger.debug(f"Authorization header em formato inválido: {header}")
                return JsonResponse(
                    {"detail": "Formato de autenticação inválido. Use: Bearer <token> ou JWT <token>"},
                    status=401
                )
                
            token = header_parts[1]
            
            # Verificar se o token está na blacklist antes de validar
            if BlacklistedTokens.objects.filter(token=token).exists():
                logger.warning(f"Token blacklisted utilizado: {token[:10]}...")
                return JsonResponse(
                    {"detail": "Token foi invalidado."},
                    status=401
                )
            
            # Validar o token
            validated_token = self.jwt_auth.get_validated_token(token.encode('utf-8'))
            request.user = self.jwt_auth.get_user(validated_token)
            
        except (InvalidToken, TokenError) as e:
            logger.warning(f"Token inválido ou expirado: {str(e)}")
            return JsonResponse(
                {"detail": "Token inválido ou expirado."},
                status=401
            )
        except Exception as e:
            logger.error(f"Erro inesperado na autenticação: {str(e)}")
            return JsonResponse(
                {"detail": "Erro na autenticação."},
                status=401
            )

        # Verificar se o usuário está autenticado
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"detail": "Autenticação necessária"}, status=401)
        
        # Administradores têm acesso total
        if user.is_superuser or (hasattr(user, 'role') and user.role == 'ADMIN'):
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
                'message': 'Você não tem permissão para acessar este recurso'
            }, status=403)
        
        return None

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
