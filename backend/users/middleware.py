from django.http import JsonResponse
from django.urls import resolve
from django.conf import settings

class PermissionMiddleware:
    """
    Middleware para verificar permissões de acesso baseadas em papel do usuário.
    Verifica se o usuário tem permissão para acessar determinados endpoints com base
    no seu papel e perfis de acesso.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Endpoints que não requerem verificação de permissão
        self.public_paths = [
            '/api/auth/login/',
            '/api/auth/register/',
            '/api/auth/refresh-token/',
            '/api/auth/password-reset/',
            '/api/auth/password-reset/confirm/',
            '/admin/',
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
        # Verificar se o caminho é público
        if any(request.path.startswith(path) for path in self.public_paths):
            return self.get_response(request)
        
        # Verificar se o usuário está autenticado
        if not request.user.is_authenticated:
            return JsonResponse({
                'error': 'Unauthorized',
                'message': 'Authentication required'
            }, status=401)
        
        # Verificar se a conta do usuário está bloqueada
        if request.user.is_locked:
            return JsonResponse({
                'error': 'Account Locked',
                'message': 'Your account has been locked due to multiple failed login attempts. Please contact an administrator.'
            }, status=403)
        
        # Administradores têm acesso total
        if request.user.is_superuser or request.user.role == 'ADMIN':
            return self.get_response(request)
        
        # Encontrar permissão necessária para o endpoint
        permission_required = None
        for pattern, permission in self.url_permission_map.items():
            import re
            if re.match(pattern, request.path):
                permission_required = permission
                break
        
        # Se não encontrou permissão necessária, permitir acesso (pode ser um endpoint não mapeado)
        if not permission_required:
            return self.get_response(request)
        
        # Verificar se o usuário tem permissão
        if request.user.has_permission(permission_required['module'], permission_required['action']):
            return self.get_response(request)
        
        # Registrar tentativa de acesso não autorizado
        from django.utils import timezone
        from users.models import AccessAttempt
        
        AccessAttempt.objects.create(
            user=request.user,
            endpoint=request.path,
            method=request.method,
            ip_address=self.get_client_ip(request),
            timestamp=timezone.now(),
            success=False
        )
        
        # Retornar erro de permissão negada
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
