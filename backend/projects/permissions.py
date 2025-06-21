"""
Custom permissions for the projects app.
Implements fine-grained access control based on project membership and roles.
"""
from rest_framework import permissions
from .models import MembroProjeto


class IsProjectMember(permissions.BasePermission):
    """
    Permission to check if user is a member of the project.
    """
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        # Get project from the object
        projeto = getattr(obj, 'projeto', obj)
        
        return MembroProjeto.objects.filter(
            projeto=projeto,
            usuario=request.user
        ).exists()


class IsProjectAdminOrOwner(permissions.BasePermission):
    """
    Permission to check if user is project admin or owner.
    """
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        # Get project from the object
        projeto = getattr(obj, 'projeto', obj)
        
        # Check if user is project creator
        if projeto.criado_por == request.user:
            return True
        
        # Check if user is project admin
        return MembroProjeto.objects.filter(
            projeto=projeto,
            usuario=request.user,
            papel='administrador'
        ).exists()


class CanManageProjectMembers(permissions.BasePermission):
    """
    Permission to manage project members.
    Only project admins and owners can add/remove members.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # For list/create actions on members
        if hasattr(view, 'get_projeto'):
            projeto = view.get_projeto()
            if projeto:
                return self._can_manage_members(request.user, projeto)
        
        return True  # Let object-level permission handle it
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        # For member objects, check the project
        projeto = obj.projeto
        return self._can_manage_members(request.user, projeto)
    
    def _can_manage_members(self, user, projeto):
        """Helper method to check if user can manage project members."""
        # Project creator can always manage
        if projeto.criado_por == user:
            return True
        
        # Project admins can manage
        return MembroProjeto.objects.filter(
            projeto=projeto,
            usuario=user,
            papel='administrador'
        ).exists()


class CanEditProject(permissions.BasePermission):
    """
    Permission for editing projects.
    Members can view, admins and owners can edit.
    """
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        projeto = obj if hasattr(obj, 'criado_por') else obj.projeto
        
        # Read permissions for project members
        if request.method in permissions.SAFE_METHODS:
            return MembroProjeto.objects.filter(
                projeto=projeto,
                usuario=request.user
            ).exists()
        
        # Write permissions for admins and owners
        if projeto.criado_por == request.user:
            return True
        
        return MembroProjeto.objects.filter(
            projeto=projeto,
            usuario=request.user,
            papel='administrador'
        ).exists()


class CanManageSprints(permissions.BasePermission):
    """
    Permission for managing sprints.
    Project members can view, admins can create/edit.
    """
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        projeto = obj.projeto
        
        # Read permissions for project members
        if request.method in permissions.SAFE_METHODS:
            return MembroProjeto.objects.filter(
                projeto=projeto,
                usuario=request.user
            ).exists()
        
        # Write permissions for admins and owners
        if projeto.criado_por == request.user:
            return True
        
        return MembroProjeto.objects.filter(
            projeto=projeto,
            usuario=request.user,
            papel__in=['administrador', 'scrum_master']
        ).exists()
