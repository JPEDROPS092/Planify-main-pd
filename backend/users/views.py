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
            # Apenas admins podem criar usuários
            return [HasModulePermission('USERS', 'CREATE')()]
        elif self.action == 'request_password_reset' or self.action == 'confirm_password_reset':
            # Qualquer pessoa pode solicitar ou confirmar um reset de senha
            return [AllowAny()]
        elif self.action in ['update', 'partial_update']:
            return [HasModulePermission('USERS', 'EDIT')()]
            return [HasModulePermission('USERS', 'EDIT')()]
        elif self.action == 'destroy':
            return [HasModulePermission('USERS', 'DELETE')()]
        elif self.action == 'list':
            # Apenas admins podem listar usuários
            return [HasModulePermission('USERS', 'VIEW')()]
        elif self.action == 'retrieve':
            return [HasModulePermission('USERS', 'VIEW')()]
        elif self.action in ['activate', 'deactivate', 'unlock']:
            return [HasModulePermission('USERS', 'EDIT')()]
        # Ações pessoais do usuário (me, permissions, change_password) só precisam de autenticação
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

    @extend_schema(
        summary="Solicitar redefinição de senha",
        tags=["Usuários"],
        description="Envia um email com um link para redefinição de senha.",
        request=ResetPasswordSerializer,
        responses={200: None}
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def request_password_reset(self, request):
        """
        Envia um email com um link para redefinição de senha.
        """
        serializer = ResetPasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                email = serializer.validated_data['email']
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    # Não informamos que o usuário não existe para evitar enumeração de contas
                    return Response({'detail': 'Se o email estiver registrado, você receberá um link para redefinição de senha.'})
                
                # Gerar token e link para reset
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Construir link
                frontend_url = settings.FRONTEND_URL.rstrip('/')
                reset_link = f"{frontend_url}/reset-password/{uid}/{token}/"
                
                # Enviar email
                from .utils import send_password_reset_email
                sent = send_password_reset_email(user, reset_link)
                
                if sent:
                    logger.info(f"Email de redefinição de senha enviado para {email}")
                    return Response({'detail': 'Se o email estiver registrado, você receberá um link para redefinição de senha.'})
                else:
                    logger.error(f"Falha ao enviar email de redefinição de senha para {email}")
                    return Response({'detail': 'Erro ao enviar email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    
            except Exception as e:
                logger.error(f"Erro ao processar redefinição de senha: {str(e)}")
                return Response({'detail': 'Erro ao processar solicitação'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Confirmar redefinição de senha",
        tags=["Usuários"],
        description="Redefine a senha do usuário usando o token e UID recebidos por email.",
        request=SetNewPasswordSerializer,
        responses={200: None}
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def confirm_password_reset(self, request):
        """
        Redefine a senha do usuário usando o token e UID recebidos por email.
        """
        serializer = SetNewPasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                password = serializer.validated_data['password']
                token = serializer.validated_data['token']
                uid = serializer.validated_data['uid']
                
                try:
                    user_id = force_str(urlsafe_base64_decode(uid))
                    user = User.objects.get(pk=user_id)
                except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                    return Response({'detail': 'Link inválido'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Validar token
                if not default_token_generator.check_token(user, token):
                    return Response({'detail': 'Token inválido ou expirado'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Atualizar senha
                update_user_password(user, password)
                
                logger.info(f"Senha redefinida com sucesso para usuário {user.get_username()} (ID: {user.pk})")
                return Response({'detail': 'Senha redefinida com sucesso'})
                
            except Exception as e:
                logger.error(f"Erro ao redefinir senha: {str(e)}")
                return Response({'detail': 'Erro ao redefinir senha'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Resetar senha (Admin)",
        tags=["Usuários"],
        description="Permite um administrador resetar a senha de um usuário.",
        responses={200: None}
    )
    @action(detail=True, methods=['post'], permission_classes=[HasModulePermission('USERS', 'EDIT')])
    def reset_password(self, request, pk=None):
        """
        Reseta a senha de um usuário e envia a nova senha por email.
        Esta é uma funcionalidade administrativa.
        
        Nota: Esta abordagem envia a senha por email, o que não é recomendado.
        Use os endpoints request_password_reset e confirm_password_reset para
        o fluxo seguro de redefinição de senha.
        """
        from .utils import generate_secure_password
        
        user = self.get_object()
        
        # Gerar nova senha
        new_password = generate_secure_password()
        
        # Atualizar senha do usuário
        user.set_password(new_password)
        user.save()
        
        # Marcar que a mudança de senha é obrigatória
        if hasattr(user, 'profile'):
            user.profile.password_change_required = True
            user.profile.save()
        
        # Enviar email com a nova senha
        subject = 'Nova senha - Planify'
        message = f'Sua senha foi redefinida por um administrador. Sua nova senha é: {new_password}'
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        
        try:
            send_mail(subject, message, email_from, recipient_list)
            logger.info(f"Email com nova senha enviado para usuário {user.get_username()}")
            return Response({'detail': 'Senha redefinida com sucesso. Um email foi enviado ao usuário.'})
        except Exception as e:
            logger.error(f"Erro ao enviar email com nova senha: {str(e)}")
            return Response(
                {'detail': 'Senha redefinida, mas houve um erro ao enviar o email. Entre em contato com o usuário.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
    
    def perform_create(self, serializer):
        # Definir automaticamente o usuário atual
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        # Usuários só podem ver seus próprios perfis
        return UserProfile.objects.filter(user=self.request.user)
    
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
    
    def get_permissions(self):
        """Define permissões com base na ação."""
        # Apenas admins podem gerenciar permissões
        return [HasModulePermission('USERS', 'EDIT')()]

@extend_schema_view(
    list=extend_schema(
        summary="Listar perfis de acesso",
        tags=["Perfis de Acesso"],
        description="Retorna uma lista paginada de perfis de acesso.",
        responses={200: AccessProfileSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Obter detalhes do perfil de acesso",
        tags=["Perfis de Acesso"],
        description="Retorna informações detalhadas de um perfil de acesso específico.",
        responses={200: AccessProfileSerializer}
    ),
    create=extend_schema(
        summary="Criar novo perfil de acesso",
        tags=["Perfis de Acesso"],
        description="Cria um novo perfil de acesso.",
        responses={201: AccessProfileSerializer}
    ),
    update=extend_schema(
        summary="Atualizar perfil de acesso",
        tags=["Perfis de Acesso"],
        description="Atualiza todos os campos de um perfil de acesso existente.",
        responses={200: AccessProfileSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualizar perfil de acesso parcialmente",
        tags=["Perfis de Acesso"],
        description="Atualiza parcialmente um perfil de acesso existente.",
        responses={200: AccessProfileSerializer}
    ),
    destroy=extend_schema(
        summary="Excluir perfil de acesso",
        tags=["Perfis de Acesso"],
        description="Remove um perfil de acesso existente.",
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
            return [HasModulePermission('USERS', 'VIEW')()]
        return [HasModulePermission('USERS', 'EDIT')()]



User = get_user_model()
logger = logging.getLogger(__name__)

@extend_schema(
    tags=['Usuários'],
    summary="Registrar novo usuário",
    description='''
    Permite o registro público de novos usuários no sistema.
    
    - Qualquer pessoa pode criar uma conta sem necessidade de autenticação prévia
    - O papel padrão atribuído é TEAM_MEMBER se não especificado
    - Um perfil de usuário é criado automaticamente
    - Retorna os dados básicos do usuário criado
    ''',
    request=UserCreateSerializer,
    responses={
        201: inline_serializer(
            name='RegisterSuccessResponse',
            fields={
                'detail': serializers.CharField(),
                'user_id': serializers.IntegerField(),
                'username': serializers.CharField(),
                'email': serializers.EmailField(),
                'role': serializers.CharField(),
            }
        ),
        400: OpenApiResponse(
            description="Dados inválidos ou erro de validação",
            response=inline_serializer(
                name='RegisterErrorResponse',
                fields={
                    'field_name': serializers.ListField(child=serializers.CharField()),
                }
            )
        )
    }
)
class RegisterView(generics.CreateAPIView):
    """
    View para registro público de usuários.
    Permite que qualquer pessoa crie uma conta sem necessidade de autenticação prévia.
    """
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        """
        Cria um novo usuário e seu perfil associado.
        """
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            try:
                # Criar o usuário (o serializer já gerencia a criação do perfil)
                user = serializer.save()
                logger.info(f"Novo usuário registrado: {user.username} (ID: {user.id})")
                
                # Retornar resposta de sucesso
                return Response({
                    'detail': 'Usuário registrado com sucesso',
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                logger.error(f"Erro ao registrar usuário: {str(e)}")
                return Response({
                    'detail': 'Erro interno do servidor durante o registro',
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
