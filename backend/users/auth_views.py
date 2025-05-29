from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.utils import timezone
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Tenta obter o usuário pelo nome de usuário
        username = attrs.get(self.username_field)
        try:
            user = User.objects.get(username=username)
            
            # Verifica se a conta está bloqueada
            if user.is_locked:
                logger.warning(f"Tentativa de login em conta bloqueada: {username}")
                raise Exception("Account is locked due to multiple failed login attempts. Please contact an administrator.")
            
            # Tenta validar as credenciais
            try:
                data = super().validate(attrs)
                
                # Login bem-sucedido, reseta o contador de tentativas
                user.reset_failed_login()
                logger.info(f"Login bem-sucedido para o usuário: {username}")
                
                # Adiciona informações extras ao token
                data['user_id'] = user.id
                data['username'] = user.username
                data['email'] = user.email
                data['role'] = user.role
                
                return data
                
            except Exception as e:
                # Login falhou, incrementa o contador de tentativas
                user.increment_failed_login()
                logger.warning(f"Tentativa de login falhou para o usuário: {username}. Tentativa {user.failed_login_attempts} de 5.")
                
                if user.is_locked:
                    logger.warning(f"Conta bloqueada após múltiplas tentativas: {username}")
                    raise Exception("Account is now locked due to multiple failed login attempts. Please contact an administrator.")
                
                # Re-lança a exceção original
                raise e
                
        except User.DoesNotExist:
            # Usuário não existe, continua com a validação normal que irá falhar
            logger.warning(f"Tentativa de login com usuário inexistente: {username}")
            return super().validate(attrs)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return response
        except Exception as e:
            error_message = str(e)
            
            if "Account is locked" in error_message:
                return Response(
                    {"detail": error_message},
                    status=status.HTTP_403_FORBIDDEN
                )
            elif "No active account found" in error_message:
                return Response(
                    {"detail": "Invalid username or password"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            else:
                logger.error(f"Erro durante autenticação: {error_message}")
                return Response(
                    {"detail": "Authentication failed"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
