"""
Custom permissions for the tasks app.
Implements task-level access control based on project membership and assignments.
"""
from rest_framework import permissions
from projects.models import MembroProjeto


class CanViewTask(permissions.BasePermission):
    """
    Permission to view tasks.
    Project members can view all project tasks.
    """
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        # Check if user is a member of the project
        return MembroProjeto.objects.filter(
            projeto=obj.projeto,
            usuario=request.user
        ).exists()


class CanEditTask(permissions.BasePermission):
    """
    Permission to edit tasks.
    Task assignees, project admins, and task creators can edit.
    """
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        # Read permissions for project members
        if request.method in permissions.SAFE_METHODS:
            return MembroProjeto.objects.filter(
                projeto=obj.projeto,
                usuario=request.user
            ).exists()
        
        # Task creator can edit
        if hasattr(obj, 'criado_por') and obj.criado_por == request.user:
            return True
        
        # Task assignees can edit
        if obj.atribuicoes.filter(usuario=request.user).exists():
            return True
        
        # Project admins can edit
        return MembroProjeto.objects.filter(
            projeto=obj.projeto,
            usuario=request.user,
            papel='administrador'
        ).exists()


class CanAssignTask(permissions.BasePermission):
    """
    Permission to assign/unassign tasks.
    Project admins and task creators can manage assignments.
    """
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        # Get the task (obj might be the task or an assignment)
        tarefa = getattr(obj, 'tarefa', obj)
        
        # Task creator can manage assignments
        if hasattr(tarefa, 'criado_por') and tarefa.criado_por == request.user:
            return True
        
        # Project admins can manage assignments
        return MembroProjeto.objects.filter(
            projeto=tarefa.projeto,
            usuario=request.user,
            papel='administrador'
        ).exists()


class CanCommentOnTask(permissions.BasePermission):
    """
    Permission to comment on tasks.
    Project members can comment.
    """
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        # Get the task (obj might be the task or a comment)
        tarefa = getattr(obj, 'tarefa', obj)
        
        # Project members can comment
        return MembroProjeto.objects.filter(
            projeto=tarefa.projeto,
            usuario=request.user
        ).exists()


class CanEditComment(permissions.BasePermission):
    """
    Permission to edit/delete comments.
    Only comment authors can edit their comments.
    """
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        # Read permissions for project members
        if request.method in permissions.SAFE_METHODS:
            return MembroProjeto.objects.filter(
                projeto=obj.tarefa.projeto,
                usuario=request.user
            ).exists()
        
        # Only comment author can edit/delete
        return obj.autor == request.user


class CanChangeTaskStatus(permissions.BasePermission):
    """
    Permission to change task status.
    Task assignees and project admins can change status.
    """
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        # Task assignees can change status
        if obj.atribuicoes.filter(usuario=request.user).exists():
            return True
        
        # Project admins can change status
        return MembroProjeto.objects.filter(
            projeto=obj.projeto,
            usuario=request.user,
            papel='administrador'
        ).exists()
