from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
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
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Retorna as informações do usuário autenticado.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
        
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def permissions(self, request):
        """
        Retorna as permissões do usuário autenticado.
        """
        user = request.user
        
        # Obter todos os perfis de acesso do usuário
        user_access_profiles = UserAccessProfile.objects.filter(user=user)
        access_profile_ids = [uap.access_profile_id for uap in user_access_profiles]
        
        # Obter todas as permissões associadas a esses perfis de acesso
        permissions = Permission.objects.filter(access_profile_id__in=access_profile_ids)
        
        # Formatar as permissões como uma lista de strings no formato "MODULO.ACAO"
        formatted_permissions = [f"{perm.module}.{perm.action}" for perm in permissions]
        
        return Response({
            'role': user.role,
            'permissions': formatted_permissions
        })
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Altera a senha do usuário autenticado."""
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Senha alterada com sucesso para o usuário: {user.username} (ID: {user.id})")
            return Response({'detail': 'Senha alterada com sucesso'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[HasModulePermission('USERS', 'EDIT')])
    def reset_password(self, request, pk=None):
        """Redefine a senha do usuário para uma senha temporária e envia por e-mail."""
        user = self.get_object()
        # Generate a temporary password
        temp_password = User.objects.make_random_password()
        
        # Usar a função utilitária para atualizar a senha
        user = update_user_password(user, temp_password)
        
        # Marcar que a senha precisa ser alterada no próximo login
        user.password_change_required = True
        user.save()
        
        # Send email with temporary password
        send_mail(
            'Redefinição de Senha',
            f'Sua senha temporária é: {temp_password}\nPor favor, altere-a após fazer login.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        logger.info(f"Senha temporária enviada para o usuário: {user.username} (ID: {user.id})")
        return Response({'detail': 'Senha temporária enviada para o e-mail do usuário'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[HasModulePermission('USERS', 'EDIT')])
    def activate(self, request, pk=None):
        """Ativa um usuário."""
        user = self.get_object()
        user.is_active = True
        user.save()
        logger.info(f"Usuário ativado: {user.username} (ID: {user.id})")
        return Response({'detail': 'Usuário ativado com sucesso'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[HasModulePermission('USERS', 'EDIT')])
    def deactivate(self, request, pk=None):
        """Desativa um usuário."""
        user = self.get_object()
        user.is_active = False
        user.save()
        logger.info(f"Usuário desativado: {user.username} (ID: {user.id})")
        return Response({'detail': 'Usuário desativado com sucesso'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[HasModulePermission('USERS', 'EDIT')])
    def unlock(self, request, pk=None):
        """Desbloqueia um usuário após tentativas de login malsucedidas."""
        user = self.get_object()
        user.is_locked = False
        user.failed_login_attempts = 0
        user.save()
        logger.info(f"Usuário desbloqueado: {user.username} (ID: {user.id})")
        return Response({'detail': 'Usuário desbloqueado com sucesso'}, status=status.HTTP_200_OK)


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccessProfileViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento de perfis de acesso."""
    queryset = AccessProfile.objects.all()
    serializer_class = AccessProfileSerializer
    permission_classes = [HasModulePermission('USERS', 'EDIT')]


class PermissionViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento de permissões."""
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [HasModulePermission('USERS', 'EDIT')]
    filterset_fields = ['access_profile', 'module', 'action']


class UserAccessProfileViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento de associações entre usuários e perfis de acesso."""
    serializer_class = UserAccessProfileSerializer
    permission_classes = [HasModulePermission('USERS', 'EDIT')]
    
    def get_queryset(self):
        """Retorna todas as associações entre usuários e perfis de acesso."""
        return UserAccessProfile.objects.all()
    
    def perform_create(self, serializer):
        """Cria uma nova associação entre usuário e perfil de acesso."""
        user_id = self.kwargs.get('user_pk')
        serializer.save(user_id=user_id)
        logger.info(f"Perfil de acesso atribuído ao usuário ID: {user_id}")


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            # Generate token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Send email with reset link
            reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            send_mail(
                'Password Reset Request',
                f'Please click the following link to reset your password: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            
            return Response({'detail': 'Password reset email has been sent'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # Don't reveal that the user doesn't exist
            return Response({'detail': 'Password reset email has been sent'}, status=status.HTTP_200_OK)


class ResetPasswordConfirmView(generics.GenericAPIView):
    """View para confirmar a redefinição de senha com token."""
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Processa a redefinição de senha com token."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            token = serializer.validated_data['token']
            password = serializer.validated_data['password']
            
            # Extract UID and token
            uid, token = token.split('/')
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
            
            if default_token_generator.check_token(user, token):
                # Usar a função utilitária para atualizar a senha
                update_user_password(user, password)
                
                logger.info(f"Senha redefinida com sucesso para o usuário: {user.username} (ID: {user.id})")
                return Response({'detail': 'Senha redefinida com sucesso'}, status=status.HTTP_200_OK)
            else:
                logger.warning(f"Tentativa de redefinição de senha com token inválido para o usuário ID: {uid}")
                return Response({'detail': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Erro ao redefinir senha: {str(e)}")
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
