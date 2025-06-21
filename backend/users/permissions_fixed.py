"""
Módulo de permissões centralizado para o sistema Planify.
Contém funções e classes para verificação e gerenciamento de permissões.
"""
import re
import logging
from django.urls import resolve
from django.conf import settings
from rest_framework.permissions import BasePermission

logger = logging.getLogger(__name__)

# Mapeamento de padrões de URL para permissões necessárias
# Formato: (regex_pattern, module, action)
URL_PERMISSION_MAPPING = [
    # Projetos
    (r'^/api/projects/?$', 'PROJECTS', 'VIEW'),
    (r'^/api/projects/\d+/?$', 'PROJECTS', 'VIEW'),
    (r'^/api/projects/\d+/edit/?$', 'PROJECTS', 'EDIT'),
    (r'^/api/projects/\d+/delete/?$', 'PROJECTS', 'DELETE'),
    
    # Tarefas
    (r'^/api/tasks/?$', 'TASKS', 'VIEW'),
    (r'^/api/tasks/\d+/?$', 'TASKS', 'VIEW'),
    (r'^/api/tasks/\d+/edit/?$', 'TASKS', 'EDIT'),
    (r'^/api/tasks/\d+/delete/?$', 'TASKS', 'DELETE'),
    
    # Equipes
    (r'^/api/teams/?$', 'TEAMS', 'VIEW'),
    (r'^/api/teams/\d+/?$', 'TEAMS', 'VIEW'),
    (r'^/api/teams/\d+/edit/?$', 'TEAMS', 'EDIT'),
    (r'^/api/teams/\d+/delete/?$', 'TEAMS', 'DELETE'),
    
    # Usuários (apenas admin)
    (r'^/api/users/?$', 'USERS', 'VIEW'),
    (r'^/api/users/\d+/?$', 'USERS', 'VIEW'),
    (r'^/api/users/\d+/edit/?$', 'USERS', 'EDIT'),
    (r'^/api/users/\d+/delete/?$', 'USERS', 'DELETE'),
    
    # Custos
    (r'^/api/costs/?$', 'COSTS', 'VIEW'),
    (r'^/api/costs/\d+/?$', 'COSTS', 'VIEW'),
    (r'^/api/costs/\d+/edit/?$', 'COSTS', 'EDIT'),
    (r'^/api/costs/\d+/delete/?$', 'COSTS', 'DELETE'),
    
    # Riscos
    (r'^/api/risks/?$', 'RISKS', 'VIEW'),
    (r'^/api/risks/\d+/?$', 'RISKS', 'VIEW'),
    (r'^/api/risks/\d+/edit/?$', 'RISKS', 'EDIT'),
    (r'^/api/risks/\d+/delete/?$', 'RISKS', 'DELETE'),
    
    # Documentos
    (r'^/api/documents/?$', 'DOCUMENTS', 'VIEW'),
    (r'^/api/documents/\d+/?$', 'DOCUMENTS', 'VIEW'),
    (r'^/api/documents/\d+/edit/?$', 'DOCUMENTS', 'EDIT'),
    (r'^/api/documents/\d+/delete/?$', 'DOCUMENTS', 'DELETE'),
    
    # Comunicações
    (r'^/api/communications/?$', 'COMMUNICATIONS', 'VIEW'),
    (r'^/api/communications/\d+/?$', 'COMMUNICATIONS', 'VIEW'),
    (r'^/api/communications/\d+/edit/?$', 'COMMUNICATIONS', 'EDIT'),
    (r'^/api/communications/\d+/delete/?$', 'COMMUNICATIONS', 'DELETE'),
]

# Caminhos públicos que não requerem autenticação
PUBLIC_PATHS = [
    # Autenticação
    r'^/api/login/?$',
    r'^/api/token/refresh/?$',
    r'^/api/logout/?$',
    r'^/api/register/?$',
    
    # Documentação da API
    r'^/api/?$',
    r'^/api/docs/?$',
    r'^/api/schema/?$',
    r'^/api/schema/swagger-ui/?$',
    r'^/api/schema/redoc/?$',
    
    # Health checks e utilitários
    r'^/api/health/?$',
    r'^/api/health/detailed/?$',
    
    # Admin do Django
    r'^/admin/.*$',
    
    # Arquivos estáticos e mídia
    r'^/static/.*$',
    r'^/media/.*$',
    
    # Debug toolbar (apenas em desenvolvimento)
    r'^/__debug__/.*$',
    
    # Favicon e outros recursos comuns
    r'^/favicon\.ico$',
]


def get_required_permission(path):
    """
    Determina a permissão necessária para um caminho específico.
    
    Args:
        path: Caminho da URL a ser verificado
        
    Returns:
        tuple: (module, action) ou None se não for necessária permissão
    """
    # Verificar se é um caminho público primeiro
    for pattern in PUBLIC_PATHS:
        if re.match(pattern, path):
            return None
    
    # Verificar mapeamentos de permissões
    for pattern, module, action in URL_PERMISSION_MAPPING:
        if re.match(pattern, path):
            return (module, action)
    
    # Se não encontrou mapeamento específico, não requer permissão
    return None


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
    # Administradores têm acesso total
    if user.is_superuser or (hasattr(user, 'role') and user.role == 'ADMIN'):
        return True
    
    # Verificar permissão específica através do método do usuário
    if hasattr(user, 'has_permission'):
        return user.has_permission(module, action)
    
    # Fallback: permitir acesso se não há sistema de permissões configurado
    return True


def log_unauthorized_access(user, path, module, action):
    """
    Registra tentativas de acesso não autorizado.
    
    Args:
        user: Usuário que tentou acessar
        path: Caminho que o usuário tentou acessar
        module: Módulo relacionado
        action: Ação tentada
    """
    logger.warning(
        "Acesso não autorizado: Usuário %s (ID: %s) tentou acessar %s sem permissão %s.%s",
        getattr(user, 'username', 'unknown'), 
        getattr(user, 'id', 'unknown'), 
        path, 
        module, 
        action
    )


class HasModulePermission(BasePermission):
    """
    Permissão personalizada para verificar se o usuário tem permissão para um módulo e ação específicos.
    """
    module = None
    action = None
    
    def __new__(cls, module=None, action=None):
        """
        Cria uma nova instância da classe com os parâmetros fornecidos.
        """
        instance = super(HasModulePermission, cls).__new__(cls)
        if module is not None:
            instance.module = module
        if action is not None:
            instance.action = action
        return instance
    
    def __init__(self, module=None, action=None):
        """
        Inicializa a instância com os parâmetros fornecidos.
        """
        self.initialized = True
        if module is not None:
            self.module = module
        if action is not None:
            self.action = action
    
    def __call__(self):
        """
        Make the permission class callable.
        """
        return self
    
    def has_permission(self, request, view):
        user = request.user
        
        # Verificar se o módulo e a ação estão definidos
        if not self.module or not self.action:
            return False
        
        # Verificar se o usuário está autenticado
        if not user or not user.is_authenticated:
            return False
        
        # Verificar se a conta está bloqueada
        if hasattr(user, 'is_locked') and user.is_locked:
            return False
        
        # Verificar permissão
        has_perm = check_user_permission(user, self.module, self.action)
        
        # Registrar tentativa de acesso não autorizado
        if not has_perm:
            log_unauthorized_access(user, request.path, self.module, self.action)
        
        return has_perm
