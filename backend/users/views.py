from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
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
    UserSerializer, UserCreateSerializer, ChangePasswordSerializer,
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
    
    def get_serializer_class(self):
        """Seleciona o serializer apropriado com base na ação."""
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_permissions(self):
        """Define permissões com base na ação."""
        if self.action == 'create':
            return [HasModulePermission('USERS', 'CREATE')]
        elif self.action == 'reset_password':
            return [HasModulePermission('USERS', 'EDIT')]
        elif self.action in ['update', 'partial_update']:
            return [HasModulePermission('USERS', 'EDIT')]
        elif self.action == 'destroy':
            return [HasModulePermission('USERS', 'DELETE')]
        elif self.action == 'list':
            return [HasModulePermission('USERS', 'VIEW')]
        return [IsAuthenticated()]
    
    @extend_schema(
        summary="Retornar minhas informações",
        tags=["Perfil"],
        description="Retorna as informações do usuário autenticado.",
        responses={200: UserSerializer}
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Retorna as informações do usuário autenticado."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @extend_schema(
        summary="Retornar minhas permissões",
        tags=["Perfil"],
        description="Retorna as permissões do usuário autenticado.",
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
        summary="Alterar senha",
        tags=["Perfil"],
        description="Altera a senha do usuário autenticado.",
        request=ChangePasswordSerializer,
        responses={200: None}
    )
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Altera a senha do usuário autenticado."""
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Senha alterada com sucesso'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Redefinir senha",
        tags=["Usuários"],
        description="Redefine a senha do usuário para uma senha temporária.",
        responses={200: None}
    )
    @action(detail=True, methods=['post'], permission_classes=[HasModulePermission('USERS', 'EDIT')])
    def reset_password(self, request, pk=None):
        """Redefine a senha do usuário para uma senha temporária."""
        user = self.get_object()
        temp_password = User.objects.make_random_password()
        user = update_user_password(user, temp_password)
        user.password_change_required = True
        user.save()
        
        send_mail(
            'Redefinição de Senha',
            f'Sua senha temporária é: {temp_password}\nPor favor, altere-a após fazer login.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        return Response({'detail': 'Senha temporária enviada para o e-mail do usuário'})

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

@extend_schema_view(
    list=extend_schema(
        summary="Listar perfis",
        tags=["Perfis"],
        description="Retorna uma lista paginada de perfis.",
        responses={200: UserProfileSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Obter detalhes do perfil",
        tags=["Perfis"],
        description="Retorna informações detalhadas de um perfil específico.",
        responses={200: UserProfileSerializer}
    ),
    create=extend_schema(
        summary="Criar novo perfil",
        tags=["Perfis"],
        description="Cria um novo perfil.",
        responses={201: UserProfileSerializer}
    ),
    update=extend_schema(
        summary="Atualizar perfil",
        tags=["Perfis"],
        description="Atualiza todos os campos de um perfil existente.",
        responses={200: UserProfileSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualizar perfil parcialmente",
        tags=["Perfis"],
        description="Atualiza parcialmente um perfil existente.",
        responses={200: UserProfileSerializer}
    ),
    destroy=extend_schema(
        summary="Excluir perfil",
        tags=["Perfis"],
        description="Remove um perfil existente.",
        responses={204: None}
    )
)
class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()

@extend_schema_view(
    list=extend_schema(
        summary="Listar permissões",
        tags=["Permissões"],
        description="Retorna uma lista paginada de permissões.",
        responses={200: PermissionSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Obter detalhes da permissão",
        tags=["Permissões"],
        description="Retorna informações detalhadas de uma permissão específica.",
        responses={200: PermissionSerializer}
    ),
    create=extend_schema(
        summary="Criar nova permissão",
        tags=["Permissões"],
        description="Cria uma nova permissão.",
        responses={201: PermissionSerializer}
    ),
    update=extend_schema(
        summary="Atualizar permissão",
        tags=["Permissões"],
        description="Atualiza todos os campos de uma permissão existente.",
        responses={200: PermissionSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualizar permissão parcialmente",
        tags=["Permissões"],
        description="Atualiza parcialmente uma permissão existente.",
        responses={200: PermissionSerializer}
    ),
    destroy=extend_schema(
        summary="Excluir permissão",
        tags=["Permissões"],
        description="Remove uma permissão existente.",
        responses={204: None}
    )
)
class PermissionViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento de permissões."""
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [HasModulePermission('USERS', 'EDIT')]
    filterset_fields = ['access_profile', 'module', 'action']
