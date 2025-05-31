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
from .models import UserProfile, AccessProfile, Permission, UserAccessProfile
from .serializers import (
    UserSerializer, UserCreateSerializer, ChangePasswordSerializer,
    ResetPasswordSerializer, SetNewPasswordSerializer, UserProfileSerializer,
    AccessProfileSerializer, PermissionSerializer, UserAccessProfileSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == 'create' or self.action == 'reset_password':
            return [IsAdminUser()]
        return super().get_permissions()
    
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
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reset_password(self, request, pk=None):
        user = self.get_object()
        # Generate a temporary password
        temp_password = User.objects.make_random_password()
        user.set_password(temp_password)
        user.password_change_required = True
        user.save()
        
        # Send email with temporary password
        send_mail(
            'Password Reset',
            f'Your temporary password is: {temp_password}\nPlease change it after logging in.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        return Response({'detail': 'Temporary password sent to user email'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def activate(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'detail': 'User activated successfully'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'detail': 'User deactivated successfully'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def unlock(self, request, pk=None):
        user = self.get_object()
        user.is_locked = False
        user.failed_login_attempts = 0
        user.save()
        return Response({'detail': 'User unlocked successfully'}, status=status.HTTP_200_OK)


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccessProfileViewSet(viewsets.ModelViewSet):
    queryset = AccessProfile.objects.all()
    serializer_class = AccessProfileSerializer
    permission_classes = [IsAdminUser]


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['access_profile', 'module', 'action']


class UserAccessProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserAccessProfileSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return UserAccessProfile.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(user_id=self.kwargs['user_pk'])


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
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
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
                user.set_password(password)
                user.password_change_required = False
                user.last_password_change = timezone.now()
                user.save()
                
                return Response({'detail': 'Password has been reset successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
