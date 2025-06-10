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
    (r'^/api/projetos/?$', 'PROJECTS', 'VIEW'),
    (r'^/api/projetos/create/?$', 'PROJECTS', 'CREATE'),
    (r'^/api/projetos/\d+/?$', 'PROJECTS', 'VIEW'),
    (r'^/api/projetos/\d+/edit/?$', 'PROJECTS', 'EDIT'),
    (r'^/api/projetos/\d+/delete/?$', 'PROJECTS', 'DELETE'),
    
    # Tarefas
    (r'^/api/projetos/\d+/tarefas/?$', 'TASKS', 'VIEW'),
    (r'^/api/projetos/\d+/tarefas/create/?$', 'TASKS', 'CREATE'),
    (r'^/api/tarefas/\d+/?$', 'TASKS', 'VIEW'),
    (r'^/api/tarefas/\d+/edit/?$', 'TASKS', 'EDIT'),
    (r'^/api/tarefas/\d+/delete/?$', 'TASKS', 'DELETE'),
    
    # Usuários (apenas admin)
    (r'^/api/users/?$', 'USERS', 'VIEW'),
    (r'^/api/users/create/?$', 'USERS', 'CREATE'),
    (r'^/api/users/\d+/?$', 'USERS', 'VIEW'),
    (r'^/api/users/\d+/edit/?$', 'USERS', 'EDIT'),
    (r'^/api/users/\d+/delete/?$', 'USERS', 'DELETE'),
]

# Caminhos públicos que não requerem autenticação
PUBLIC_PATHS = [
    # Autenticação
    r'^/api/auth/token/?$',
    r'^/api/auth/token/refresh/?$',
    r'^/api/auth/register/?$',
    r'^/api/auth/forgot-password/?$',
    r'^/api/auth/reset-password-confirm/?$',
    
    # Documentação
    r'^/api/docs/?$',
    r'^/api/schema/?$',
    r'^/api/schema/swagger-ui/?$',
    r'^/api/schema/redoc/?$',
    r'^/docs/?$',
    r'^/swagger(?:-ui)?/?$',
    r'^/redoc/?$',
    
    # Administrativo
    r'^/admin/.*$',
    r'^/static/admin/.*$',
    r'^/static/.*$',  # Arquivos estáticos
    r'^/media/.*$',   # Arquivos de mídia
    
    # Favicon e outros recursos comuns
    r'^/favicon\.ico$',
]


def get_required_permission(path):
    """
    Determina a permissão necessária para um caminho específico.

    Args:
        path (str): Caminho da URL a ser verificado.

    Returns:
        tuple: (module, action) ou None se não for necessária permissão.
    """
    for pattern in PUBLIC_PATHS:
        if re.match(pattern, path):
            return None

    for pattern, module, action in URL_PERMISSION_MAPPING:
        if re.match(pattern, path):
            return (module, action)

    return None


def check_user_permission(user, module, action):
    """
    Verifica se um usuário tem permissão para uma ação específica em um módulo.

    Args:
        user (User): Instância do modelo User.
        module (str): Módulo a ser verificado (ex: 'PROJECTS', 'TASKS').
        action (str): Ação a ser verificada (ex: 'VIEW', 'CREATE', 'EDIT', 'DELETE').

    Returns:
        bool: True se o usuário tem permissão, False caso contrário.
    """
    if user.is_superuser or user.role == 'ADMIN':
        return True

    return user.has_permission(module, action)


def log_unauthorized_access(user, path, module, action):
    """
    Registra tentativas de acesso não autorizado.

    Args:
        user (User): Usuário que tentou acessar.
        path (str): Caminho que o usuário tentou acessar.
        module (str): Módulo relacionado.
        action (str): Ação tentada.
    """
    logger.warning(
        "Acesso não autorizado: Usuário %s (ID: %s) tentou acessar %s sem permissão %s.%s",
        user.username, user.id, path, module, action
    )


class HasModulePermission(BasePermission):
    """
    Permissão personalizada para verificar se o usuário tem permissão para um módulo e ação específicos.
    """
    module = None
    action = None

    def __new__(cls, module=None, action=None):
        instance = super(HasModulePermission, cls).__new__(cls)
        if module is not None:
            instance.module = module
        if action is not None:
            instance.action = action
        return instance

    def __init__(self, module=None, action=None):
        self.initialized = True
        if module is not None:
            self.module = module
        if action is not None:
            self.action = action

    def __call__(self):
        return self

    def has_permission(self, request, view):
        user = request.user

        if not self.module or not self.action:
            return False

        if not user or not user.is_authenticated:
            return False

        if hasattr(user, 'is_locked') and user.is_locked:
            return False

        has_perm = check_user_permission(user, self.module, self.action)

        if not has_perm:
            log_unauthorized_access(user, request.path, self.module, self.action)

        return has_perm
