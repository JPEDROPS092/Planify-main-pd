from django.http import JsonResponse
from django.urls import resolve
from django.conf import settings
import logging
import re
import traceback

logger = logging.getLogger(__name__)

class PermissionMiddleware:
    """
    Middleware para verificar permissões de acesso baseadas em papel do usuário.
    Verifica se o usuário tem permissão para acessar determinados endpoints com base
    no seu papel e perfis de acesso.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Caminhos absolutamente públicos que devem ser ignorados sem nenhuma verificação
        self.absolute_public_paths = [
            '/',
            '/favicon.ico',
        ]
        
        # Prefixos de caminhos públicos
        self.public_prefixes = [
            '/static/',
            '/media/',
            '/admin/',
            '/api/docs/',
            '/api/schema/',
            '/api/auth/'
        ]
        
        # Endpoints que não requerem verificação de permissão
        self.public_paths = [
            '/',  # Rota raiz
            '/favicon.ico',  # Favicon
            '/api/docs/',  # Documentação da API
            '/api/auth/token/',  
            '/api/auth/register/',
            '/api/auth/token/refresh/',  
            '/api/auth/password-reset/',
            '/api/auth/password-reset/confirm/',
            '/admin/',
            '/admin/login/',
            # Rotas de registro público
            '/api/users/register/',
            # Adicionar endpoints do Djoser que devem ser públicos
            '/api/auth/users/', 
            '/api/auth/users/activation/',
            '/api/auth/users/resend_activation/',
            '/api/auth/users/reset_password/',
            '/api/auth/users/reset_password_confirm/',
            # Endpoints do drf-spectacular para documentação da API
            '/api/schema/',
            '/api/schema/swagger-ui/',
            '/api/schema/redoc/',
            # Arquivos estáticos
            '/static/',
            '/media/',
        ]
        
        # Mapeamento de URLs para módulos e ações
        self.url_permission_map = {
            # Projetos
            r'^/api/projects/$': {'module': 'PROJECTS', 'action': 'VIEW'},
            r'^/api/projects/[0-9]+/$': {'module': 'PROJECTS', 'action': 'VIEW'},
            r'^/api/projects/create/$': {'module': 'PROJECTS', 'action': 'CREATE'},
            r'^/api/projects/[0-9]+/edit/$': {'module': 'PROJECTS', 'action': 'EDIT'},
            r'^/api/projects/[0-9]+/delete/$': {'module': 'PROJECTS', 'action': 'DELETE'},

            # Tarefas
            r'^/api/tasks/$': {'module': 'TASKS', 'action': 'VIEW'},
            r'^/api/tasks/[0-9]+/$': {'module': 'TASKS', 'action': 'VIEW'},
            r'^/api/tasks/create/$': {'module': 'TASKS', 'action': 'CREATE'},
            r'^/api/tasks/[0-9]+/edit/$': {'module': 'TASKS', 'action': 'EDIT'},
            r'^/api/tasks/[0-9]+/delete/$': {'module': 'TASKS', 'action': 'DELETE'},
            r'^/api/tasks/[0-9]+/assign/$': {'module': 'TASKS', 'action': 'ASSIGN'},

            # Equipes
            r'^/api/teams/$': {'module': 'TEAMS', 'action': 'VIEW'},
            r'^/api/teams/[0-9]+/$': {'module': 'TEAMS', 'action': 'VIEW'},
            r'^/api/teams/create/$': {'module': 'TEAMS', 'action': 'CREATE'},
            r'^/api/teams/[0-9]+/edit/$': {'module': 'TEAMS', 'action': 'EDIT'},
            r'^/api/teams/[0-9]+/delete/$': {'module': 'TEAMS', 'action': 'DELETE'},

            # Riscos
            r'^/api/risks/$': {'module': 'RISKS', 'action': 'VIEW'},
            r'^/api/risks/[0-9]+/$': {'module': 'RISKS', 'action': 'VIEW'},
            r'^/api/risks/create/$': {'module': 'RISKS', 'action': 'CREATE'},
            r'^/api/risks/[0-9]+/edit/$': {'module': 'RISKS', 'action': 'EDIT'},
            r'^/api/risks/[0-9]+/delete/$': {'module': 'RISKS', 'action': 'DELETE'},

            # Documentos
            r'^/api/documents/$': {'module': 'DOCUMENTS', 'action': 'VIEW'},
            r'^/api/documents/[0-9]+/$': {'module': 'DOCUMENTS', 'action': 'VIEW'},
            r'^/api/documents/create/$': {'module': 'DOCUMENTS', 'action': 'CREATE'},
            r'^/api/documents/[0-9]+/edit/$': {'module': 'DOCUMENTS', 'action': 'EDIT'},
            r'^/api/documents/[0-9]+/delete/$': {'module': 'DOCUMENTS', 'action': 'DELETE'},
            r'^/api/documents/[0-9]+/approve/$': {'module': 'DOCUMENTS', 'action': 'APPROVE'},

            # Custos
            r'^/api/costs/$': {'module': 'COSTS', 'action': 'VIEW'},
            r'^/api/costs/[0-9]+/$': {'module': 'COSTS', 'action': 'VIEW'},
            r'^/api/costs/create/$': {'module': 'COSTS', 'action': 'CREATE'},
            r'^/api/costs/[0-9]+/edit/$': {'module': 'COSTS', 'action': 'EDIT'},
            r'^/api/costs/[0-9]+/delete/$': {'module': 'COSTS', 'action': 'DELETE'},

            # Comunicações
            r'^/api/communications/$': {'module': 'COMMUNICATIONS', 'action': 'VIEW'},
            r'^/api/communications/[0-9]+/$': {'module': 'COMMUNICATIONS', 'action': 'VIEW'},
            r'^/api/communications/create/$': {'module': 'COMMUNICATIONS', 'action': 'CREATE'},
            r'^/api/communications/[0-9]+/edit/$': {'module': 'COMMUNICATIONS', 'action': 'EDIT'},
            r'^/api/communications/[0-9]+/delete/$': {'module': 'COMMUNICATIONS', 'action': 'DELETE'},

            # Relatórios
            r'^/api/reports/$': {'module': 'REPORTS', 'action': 'VIEW'},
            r'^/api/reports/[0-9]+/$': {'module': 'REPORTS', 'action': 'VIEW'},
            r'^/api/reports/create/$': {'module': 'REPORTS', 'action': 'CREATE'},
            r'^/api/reports/export/$': {'module': 'REPORTS', 'action': 'EXPORT'},

            # Usuários
            r'^/api/users/$': {'module': 'USERS', 'action': 'VIEW'},
            r'^/api/users/[0-9]+/$': {'module': 'USERS', 'action': 'VIEW'},
            r'^/api/users/create/$': {'module': 'USERS', 'action': 'CREATE'},
            r'^/api/users/[0-9]+/edit/$': {'module': 'USERS', 'action': 'EDIT'},
            r'^/api/users/[0-9]+/delete/$': {'module': 'USERS', 'action': 'DELETE'},

            # Configurações
            r'^/api/settings/$': {'module': 'SETTINGS', 'action': 'VIEW'},
            r'^/api/settings/edit/$': {'module': 'SETTINGS', 'action': 'EDIT'},

            # Dashboard
            r'^/api/dashboard/$': {'module': 'DASHBOARD', 'action': 'VIEW'},

            # Notificações
            r'^/api/notifications/$': {'module': 'NOTIFICATIONS', 'action': 'VIEW'},
            r'^/api/notifications/[0-9]+/mark-read/$': {'module': 'NOTIFICATIONS', 'action': 'EDIT'},

            # Aprovações
            r'^/api/approvals/$': {'module': 'APPROVALS', 'action': 'VIEW'},
            r'^/api/approvals/[0-9]+/approve/$': {'module': 'APPROVALS', 'action': 'APPROVE'},
            r'^/api/approvals/[0-9]+/reject/$': {'module': 'APPROVALS', 'action': 'EDIT'},
        }

    def __call__(self, request):
        # Informações básicas da requisição
        logger.debug(f"Verificando permissões para: {request.path} [{request.method}]")

        # Verificar se o caminho está na lista de caminhos absolutamente públicos
        if request.path in self.absolute_public_paths:
            logger.debug(f"Caminho {request.path} é absolutamente público, permitindo acesso imediato sem verificações")
            return self.get_response(request)

        # Verificar arquivos estáticos e admin (caminhos que sempre devem ser públicos)
        if any(request.path.startswith(prefix) for prefix in ['/static/', '/media/', '/admin/']):
            logger.debug(f"Caminho {request.path} é estático ou admin, permitindo acesso imediato")
            return self.get_response(request)

        # Verificar se o caminho começa com um prefixo público
        for prefix in self.public_prefixes:
            if request.path.startswith(prefix):
                logger.debug(f"Caminho {request.path} começa com {prefix} que é público, permitindo acesso")
                return self.get_response(request)

        # Verificar se o caminho é público (correspondência exata)
        if request.path in self.public_paths:
            logger.debug(f"Caminho {request.path} é público (correspondência exata), permitindo acesso")
            return self.get_response(request)

        # Se chegou até aqui, o caminho não é público, então verificar autenticação
        auth_header = request.headers.get('Authorization')
        if auth_header:
            logger.debug(f"Header de autorização presente: {auth_header[:20]}...")
        else:
            logger.debug("Nenhum header de autorização encontrado")

        try:
            # Verificar se o usuário está autenticado
            if not hasattr(request, 'user') or not request.user.is_authenticated:
                logger.warning(f"Usuário não autenticado tentando acessar {request.path}")
                return JsonResponse({
                    'error': 'Unauthorized',
                    'message': 'Authentication required',
                    'detail': 'You must be logged in to access this resource'
                }, status=401)
        except AttributeError as e:
            logger.error(f"Erro de atributo durante autenticação no middleware: {str(e)}")
            return JsonResponse({
                'error': 'Unauthorized',
                'message': 'Authentication failed',
                'detail': 'Authentication system error'
            }, status=401)
        except Exception as e:
            logger.error(f"Erro durante autenticação no middleware: {str(e)}")
            logger.error(traceback.format_exc())
            return JsonResponse({
                'error': 'Unauthorized',
                'message': 'Authentication failed',
                'detail': 'An unexpected error occurred during authentication'
            }, status=401)

        # Log de informações do usuário autenticado
        logger.debug(f"Usuário autenticado: {request.user.username} (ID: {request.user.id})")

        # Verificar se a conta do usuário está bloqueada
        if request.user.is_locked:
            logger.warning(f"Conta do usuário {request.user.username} está bloqueada, acesso negado")
            return JsonResponse({
                'error': 'Account Locked',
                'message': 'Your account has been locked due to multiple failed login attempts. Please contact an administrator.'
            }, status=403)

        # Administradores têm acesso total
        if request.user.is_superuser or request.user.role == 'ADMIN':
            logger.debug(f"Usuário {request.user.username} é administrador, concedendo acesso total")
            return self.get_response(request)

        # Encontrar permissão necessária para o endpoint
        permission_required = None
        for pattern, permission in self.url_permission_map.items():
            import re
            if re.match(pattern, request.path):
                permission_required = permission
                logger.debug(f"Permissão necessária para {request.path}: {permission['module']}.{permission['action']}")
                break

        # Se não encontrou permissão necessária, permitir acesso (pode ser um endpoint não mapeado)
        if not permission_required:
            logger.debug(f"Nenhuma permissão específica necessária para {request.path}, concedendo acesso")
            return self.get_response(request)

        # Verificar se o usuário tem permissão
        if request.user.has_permission(permission_required['module'], permission_required['action']):
            logger.debug(f"Usuário {request.user.username} tem permissão {permission_required['module']}.{permission_required['action']}, concedendo acesso")
            return self.get_response(request)

        # Registrar tentativa de acesso não autorizado
        from django.utils import timezone
        from users.models import AccessAttempt

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
        logger.warning(f"Usuário {request.user.username} não tem permissão {permission_required['module']}.{permission_required['action']} para acessar {request.path} (IP: {client_ip})")
        return JsonResponse({
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource'
        }, status=403)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
