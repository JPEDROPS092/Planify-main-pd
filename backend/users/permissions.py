"""
Custom permissions for the users app.
Implements permission checking based on user roles and access profiles.
"""
from rest_framework import permissions


class HasModulePermission(permissions.BasePermission):
    """
    Permission class that checks if the user has permission for a specific module and action.
    """
    
    def __init__(self, module, action):
        """
        Initialize with the required module and action.
        
        Args:
            module (str): The module name (e.g., 'USERS', 'PROJECTS')
            action (str): The action name (e.g., 'VIEW', 'EDIT', 'DELETE')
        """
        self.module = module
        self.action = action
        
    def has_permission(self, request, view):
        """
        Check if the authenticated user has the required permission.
        
        Superusers always have all permissions.
        For regular users, we check their role and access profiles.
        """
        user = request.user
        
        # Unauthenticated users have no permissions
        if not user or not user.is_authenticated:
            return False
        
        # Superusers have all permissions
        if user.is_superuser:
            return True
        
        # ADMIN role has all permissions
        if getattr(user, 'role', None) == 'ADMIN':
            return True
        
        # Check user permissions based on access profiles
        try:
            from users.models import UserAccessProfile, Permission
            
            # Get all access profiles assigned to the user
            user_access_profiles = UserAccessProfile.objects.filter(user=user)
            access_profile_ids = [uap.access_profile.id for uap in user_access_profiles]
            
            # Check if any of the user's access profiles has the required permission
            return Permission.objects.filter(
                access_profile_id__in=access_profile_ids,
                module=self.module,
                action=self.action
            ).exists()
        
        except Exception:
            # If there's any error in permission checking, deny access by default
            return False
