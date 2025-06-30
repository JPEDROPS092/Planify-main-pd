from rest_framework import viewsets, status, generics, serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter,
    inline_serializer, OpenApiResponse
)
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import logging

from .models import UserProfile, AccessProfile, Permission, UserAccessProfile
from .serializers import (
    UserSerializer, UserCreateSerializer, 
    ResetPasswordSerializer, SetNewPasswordSerializer, UserProfileSerializer,
    AccessProfileSerializer, PermissionSerializer, UserAccessProfileSerializer
)
from .permissions import HasModulePermission
from .utils import update_user_password

User = get_user_model()
logger = logging.getLogger(__name__)

@extend_schema_view(
    list=extend_schema(
        summary="Listar usuários",
        tags=["Usuários"],
        description="Retorna uma lista paginada de usuários.",
        responses={200: UserSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Obter detalhes do usuário",
        tags=["Usuários"],
        description="Retorna informações detalhadas de um usuário específico.",
        responses={200: UserSerializer}
    ),
    create=extend_schema(
        summary="Criar novo usuário",
        tags=["Usuários"],
        description="Cria um novo usuário.",
        responses={201: UserCreateSerializer}
    ),
    update=extend_schema(
        summary="Atualizar usuário",
        tags=["Usuários"],
        description="Atualiza todos os campos de um usuário existente.",
        responses={200: UserSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualizar usuário parcialmente",
        tags=["Usuários"],
        description="Atualiza parcialmente um usuário existente.",
        responses={200: UserSerializer}
    ),
    destroy=extend_schema(
        summary="Excluir usuário",
        tags=["Usuários"],
        description="Remove um usuário existente.",
        responses={204: None}
    )
)
class UserViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento de usuários."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """Define permissões com base na ação."""
        if self.action == 'create':
            # Apenas admins podem criar usuários
            return [HasModulePermission('USERS', 'CREATE')]
        elif self.action == 'request_password_reset' or self.action == 'confirm_password_reset':
            # Qualquer pessoa pode solicitar ou confirmar um reset de senha
            return [AllowAny()]
        elif self.action in ['update', 'partial_update']:
            return [HasModulePermission('USERS', 'EDIT')]
        elif self.action == 'destroy':
            return [HasModulePermission('USERS', 'DELETE')]
        elif self.action == 'list':
            # Apenas admins podem listar usuários
            return [HasModulePermission('USERS', 'VIEW')]
        elif self.action == 'retrieve':
            return [HasModulePermission('USERS', 'VIEW')]
        elif self.action in ['activate', 'deactivate', 'unlock', 'reset_password']:
            return [HasModulePermission('USERS', 'EDIT')]
        # Ações pessoais do usuário (me, permissions, change_password) só precisam de autenticação
        return [IsAuthenticated()]
    
    # NOTA: As seguintes ações foram removidas pois o djoser já as fornece:
    # - me() -> disponível em /api/auth/users/me/
    # - change_password() -> disponível em /api/auth/users/set_password/
    # - reset_password() -> disponível em /api/auth/users/reset_password/
    # 
    # As ações abaixo são específicas para administração e não são cobertas pelo djoser

    @extend_schema(
        summary="Retornar minhas permissões",
        tags=["Perfil"],
        description="Retorna as permissões do usuário autenticado.",
        operation_id="users_my_permissions_list",
        responses={200: None}
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def permissions(self, request):
        """Retorna as permissões do usuário autenticado."""
        user = request.user
        user_access_profiles = UserAccessProfile.objects.filter(user=user)
        access_profile_ids = [uap.access_profile.id for uap in user_access_profiles]
        permissions = Permission.objects.filter(access_profile_id__in=access_profile_ids)
        formatted_permissions = [f"{perm.module}.{perm.action}" for perm in permissions]
        
        return Response({
            'role': user.role,
            'permissions': formatted_permissions
        })

    @extend_schema(
        summary="Ativar usuário",
        tags=["Usuários"],
        description="Ativa um usuário inativo.",
        responses={200: None}
    )
    @action(detail=True, methods=['post'], permission_classes=[HasModulePermission('USERS', 'EDIT')])
    def activate(self, request, pk=None):
        """Ativa um usuário."""
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'detail': 'Usuário ativado com sucesso'})

    @extend_schema(
        summary="Desativar usuário",
        tags=["Usuários"],
        description="Desativa um usuário ativo.",
        responses={200: None}
    )
    @action(detail=True, methods=['post'], permission_classes=[HasModulePermission('USERS', 'EDIT')])
    def deactivate(self, request, pk=None):
        """Desativa um usuário."""
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'detail': 'Usuário desativado com sucesso'})

    @extend_schema(
        summary="Desbloquear usuário",
        tags=["Usuários"],
        description="Desbloqueia um usuário após tentativas de login malsucedidas.",
        responses={200: None}
    )
    @action(detail=True, methods=['post'], permission_classes=[HasModulePermission('USERS', 'EDIT')])
    def unlock(self, request, pk=None):
        """Desbloqueia um usuário."""
        user = self.get_object()
        user.is_locked = False
        user.failed_login_attempts = 0
        user.save()
        return Response({'detail': 'Usuário desbloqueado com sucesso'})

    # NOTA: Removida a ação reset_password() pois o djoser fornece endpoints mais seguros:
    # - POST /api/auth/users/reset_password/ (solicitar reset)
    # - POST /api/auth/users/reset_password_confirm/ (confirmar reset com token)
    # Estes são mais seguros pois não enviam a senha por email

@extend_schema_view(
    list=extend_schema(
        summary="Listar perfis de usuário",
        tags=["Administração - Perfis de Usuário"],
        description="Retorna uma lista paginada de perfis de usuário.",
        operation_id="admin_user_profiles_list",
        responses={200: UserProfileSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Obter detalhes do perfil de usuário",
        tags=["Administração - Perfis de Usuário"],
        description="Retorna informações detalhadas de um perfil de usuário específico.",
        operation_id="admin_user_profiles_retrieve",
        responses={200: UserProfileSerializer}
    ),
    create=extend_schema(
        summary="Criar novo perfil de usuário",
        tags=["Administração - Perfis de Usuário"],
        description="Cria um novo perfil de usuário.",
        operation_id="admin_user_profiles_create",
        responses={201: UserProfileSerializer}
    ),
    update=extend_schema(
        summary="Atualizar perfil de usuário",
        tags=["Administração - Perfis de Usuário"],
        description="Atualiza todos os campos de um perfil de usuário existente.",
        operation_id="admin_user_profiles_update",
        responses={200: UserProfileSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualizar perfil de usuário parcialmente",
        tags=["Administração - Perfis de Usuário"],
        description="Atualiza parcialmente um perfil de usuário existente.",
        operation_id="admin_user_profiles_partial_update",
        responses={200: UserProfileSerializer}
    ),
    destroy=extend_schema(
        summary="Excluir perfil de usuário",
        tags=["Administração - Perfis de Usuário"],
        description="Remove um perfil de usuário existente.",
        operation_id="admin_user_profiles_destroy",
        responses={204: None}
    )
)
class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento de perfis de usuário."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  # No pagination for profiles
    
    def get_permissions(self):
        """Define permissões com base na ação."""
        if self.action in ['update', 'partial_update', 'destroy']:
            return [HasModulePermission('USERS', 'EDIT')]
        elif self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        # Return format expected by test
        return Response({"results": serializer.data})
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
@extend_schema_view(
    list=extend_schema(
        summary="Listar permissões do sistema",
        tags=["Administração - Permissões"],
        description="Retorna uma lista paginada de permissões do sistema.",
        operation_id="admin_permissions_list",
        responses={200: PermissionSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Obter detalhes da permissão",
        tags=["Administração - Permissões"],
        description="Retorna informações detalhadas de uma permissão específica.",
        operation_id="admin_permissions_retrieve",
        responses={200: PermissionSerializer}
    ),
    create=extend_schema(
        summary="Criar nova permissão",
        tags=["Administração - Permissões"],
        description="Cria uma nova permissão.",
        operation_id="admin_permissions_create",
        responses={201: PermissionSerializer}
    ),
    update=extend_schema(
        summary="Atualizar permissão",
        tags=["Administração - Permissões"],
        description="Atualiza todos os campos de uma permissão existente.",
        operation_id="admin_permissions_update",
        responses={200: PermissionSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualizar permissão parcialmente",
        tags=["Administração - Permissões"],
        description="Atualiza parcialmente uma permissão existente.",
        operation_id="admin_permissions_partial_update",
        responses={200: PermissionSerializer}
    ),
    destroy=extend_schema(
        summary="Excluir permissão",
        tags=["Administração - Permissões"],
        description="Remove uma permissão existente.",
        operation_id="admin_permissions_destroy",
        responses={204: None}
    )
)
class PermissionViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento de permissões."""
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filterset_fields = ['access_profile', 'module', 'action']
    pagination_class = None  # No pagination for permissions
    
    def get_permissions(self):
        """Define permissões com base na ação."""
        if self.action in ['list', 'retrieve']:
            return [HasModulePermission('USERS', 'VIEW')]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [HasModulePermission('USERS', 'EDIT')]
        return [HasModulePermission('USERS', 'EDIT')]
    
    def list(self, request, *args, **kwargs):
        # Check if user has USERS VIEW permission
        if not request.user.is_superuser and not hasattr(request.user, 'access_profiles'):
            return Response(status=status.HTTP_403_FORBIDDEN)
                
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        # Return format expected by tests
        return Response({"results": serializer.data})
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

@extend_schema_view(
    list=extend_schema(
        summary="Listar perfis de acesso",
        tags=["Administração - Perfis de Acesso"],
        description="Retorna uma lista paginada de perfis de acesso.",
        operation_id="admin_access_profiles_list",
        responses={200: AccessProfileSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Obter detalhes do perfil de acesso",
        tags=["Administração - Perfis de Acesso"],
        description="Retorna informações detalhadas de um perfil de acesso específico.",
        operation_id="admin_access_profiles_retrieve",
        responses={200: AccessProfileSerializer}
    ),
    create=extend_schema(
        summary="Criar novo perfil de acesso",
        tags=["Administração - Perfis de Acesso"],
        description="Cria um novo perfil de acesso.",
        operation_id="admin_access_profiles_create",
        responses={201: AccessProfileSerializer}
    ),
    update=extend_schema(
        summary="Atualizar perfil de acesso",
        tags=["Administração - Perfis de Acesso"],
        description="Atualiza todos os campos de um perfil de acesso existente.",
        operation_id="admin_access_profiles_update",
        responses={200: AccessProfileSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualizar perfil de acesso parcialmente",
        tags=["Administração - Perfis de Acesso"],
        description="Atualiza parcialmente um perfil de acesso existente.",
        operation_id="admin_access_profiles_partial_update",
        responses={200: AccessProfileSerializer}
    ),
    destroy=extend_schema(
        summary="Excluir perfil de acesso",
        tags=["Administração - Perfis de Acesso"],
        description="Remove um perfil de acesso existente.",
        operation_id="admin_access_profiles_destroy",
        responses={204: None}
    )
)
class AccessProfileViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento de perfis de acesso."""
    queryset = AccessProfile.objects.all()
    serializer_class = AccessProfileSerializer
    permission_classes = [HasModulePermission('USERS', 'EDIT')]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_permissions(self):
        """Define permissões com base na ação."""
        if self.action in ['list', 'retrieve']:
            return [HasModulePermission('USERS', 'VIEW')]
        return [HasModulePermission('USERS', 'EDIT')]

# NOTA: Removida a RegisterView pois o djoser fornece endpoint de registro:
# - POST /api/auth/users/ (registro com email e senha)
# O djoser usa automaticamente o serializer configurado em DJOSER['SERIALIZERS']['user_create']
