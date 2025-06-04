from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
import logging
import datetime

User = get_user_model()
logger = logging.getLogger(__name__)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Tenta obter o usuário pelo nome de usuário
        username = attrs.get(self.username_field)
        ip_address = self.context['request'].META.get('REMOTE_ADDR', 'unknown')
        
        try:
            user = User.objects.get(username=username)
            
            # Verifica se a conta está bloqueada
            if user.is_locked:
                logger.warning(f"Tentativa de login em conta bloqueada: {username} | IP: {ip_address}")
                raise Exception("Conta bloqueada devido a múltiplas tentativas de login malsucedidas. Entre em contato com um administrador.")
            
            # Tenta validar as credenciais
            try:
                data = super().validate(attrs)
                
                # Login bem-sucedido, reseta o contador de tentativas
                user.reset_failed_login()
                logger.info(f"Login bem-sucedido para o usuário: {username} | IP: {ip_address}")
                
                # Registrar acesso bem-sucedido
                from .models import AccessAttempt
                AccessAttempt.objects.create(
                    user=user,
                    endpoint='/api/auth/token/',
                    method='POST',
                    ip_address=ip_address,
                    timestamp=timezone.now(),
                    success=True
                )
                
                # Adiciona informações extras ao token
                data['user_id'] = user.id
                data['username'] = user.username
                data['email'] = user.email
                data['role'] = user.role
                data['full_name'] = user.full_name
                data['is_staff'] = user.is_staff
                data['is_superuser'] = user.is_superuser
                
                # Verificar se o usuário precisa alterar a senha
                if user.password_change_required:
                    data['password_change_required'] = True
                    
                # Verificar se a senha está expirada (se configurado)
                if hasattr(settings, 'PASSWORD_EXPIRY_DAYS') and user.last_password_change:
                    expiry_date = user.last_password_change + datetime.timedelta(days=settings.PASSWORD_EXPIRY_DAYS)
                    if timezone.now() > expiry_date:
                        data['password_expired'] = True
                
                return data
                
            except Exception as e:
                # Login falhou, incrementa o contador de tentativas
                user.increment_failed_login()
                attempts_left = 5 - user.failed_login_attempts
                logger.warning(f"Tentativa de login falhou para o usuário: {username} | IP: {ip_address} | Tentativa {user.failed_login_attempts} de 5")
                
                # Registrar acesso malsucedido
                from .models import AccessAttempt
                AccessAttempt.objects.create(
                    user=user,
                    endpoint='/api/auth/token/',
                    method='POST',
                    ip_address=ip_address,
                    timestamp=timezone.now(),
                    success=False
                )
                
                if user.is_locked:
                    logger.warning(f"Conta bloqueada após múltiplas tentativas: {username} | IP: {ip_address}")
                    raise Exception("Conta bloqueada devido a múltiplas tentativas de login malsucedidas. Entre em contato com um administrador.")
                else:
                    # Informar quantas tentativas restantes
                    raise Exception(f"Credenciais inválidas. Tentativas restantes: {attempts_left}")
                
        except User.DoesNotExist:
            # Usuário não existe, continua com a validação normal que irá falhar
            logger.warning(f"Tentativa de login com usuário inexistente: {username} | IP: {ip_address}")
            return super().validate(attrs)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return response
        except Exception as e:
            error_message = str(e)
            ip_address = request.META.get('REMOTE_ADDR', 'unknown')
            
            if "Conta bloqueada" in error_message:
                logger.error(f"Acesso bloqueado: {error_message} | IP: {ip_address}")
                return Response(
                    {
                        "status": "error",
                        "code": "account_locked",
                        "message": error_message
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            elif "Tentativas restantes" in error_message:
                return Response(
                    {
                        "status": "error",
                        "code": "invalid_credentials",
                        "message": error_message
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
            elif "No active account found" in error_message:
                logger.warning(f"Credenciais inválidas para login | IP: {ip_address}")
                return Response(
                    {
                        "status": "error",
                        "code": "invalid_credentials",
                        "message": "Nome de usuário ou senha inválidos"
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
            else:
                logger.error(f"Erro durante autenticação: {error_message} | IP: {ip_address}")
                return Response(
                    {
                        "status": "error",
                        "code": "authentication_failed",
                        "message": "Falha na autenticação. Tente novamente mais tarde."
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
