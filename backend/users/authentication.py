from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            header = self.get_header(request)
            if header is None:
                return None

            raw_token = self.get_raw_token(header)
            if raw_token is None:
                return None

            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            
            # Verificar se o token está na blacklist
            from .models import BlacklistedTokens
            if BlacklistedTokens.objects.filter(token=str(raw_token)).exists():
                logger.warning(f"Token blacklisted usado por usuário {user.username}")
                raise InvalidToken("Token foi invalidado")
            
            return (user, validated_token)
        except InvalidToken as e:
            logger.warning(f"Token inválido: {str(e)}")
            return None
        except TokenError as e:
            logger.warning(f"Erro no token: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado na autenticação: {str(e)}")
            return None

    def get_header(self, request):
        """
        Extracts the header containing the JWT from the given request.
        Aceita tanto 'Bearer' quanto 'JWT' como prefixos.
        """
        header = request.META.get('HTTP_AUTHORIZATION')
        if not header:
            return None

        # Check if header starts with JWT or Bearer
        parts = header.split()
        if len(parts) != 2:
            return None
            
        if parts[0] not in ('JWT', 'Bearer'):
            return None

        return header

    def get_raw_token(self, header):
        """
        Extracts the raw token from the authorization header.
        """
        parts = header.split()
        if len(parts) == 2:
            # Retorna como bytes se for string, caso contrário retorna como está
            token = parts[1]
            if isinstance(token, str):
                return token.encode('utf-8')
            return token
        return None


def get_tokens_for_user(user):
    """
    Generate JWT tokens for the given user
    """
    from rest_framework_simplejwt.tokens import AccessToken
    
    refresh = RefreshToken.for_user(user)
    access = AccessToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(access),
    }

from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, inline_serializer
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from .serializers import LogoutResponseSerializer
from .models import BlacklistedTokens
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

@extend_schema(
    tags=['Autenticação'],
    summary="Login de usuário",
    description='''
    Realiza o login do usuário e retorna os tokens de acesso e refresh.
    
    O token de acesso deve ser usado no header de todas as requisições:
    `Authorization: Bearer <access_token>` ou `Authorization: JWT <access_token>`
    
    Quando o token de acesso expirar (após 1 hora), use o token de refresh para obter um novo.
    ''',
    request=inline_serializer(
        name='LoginRequest',
        fields={
            'username': serializers.CharField(),
            'password': serializers.CharField(write_only=True)
        }
    ),
    responses={
        200: inline_serializer(
            name='LoginResponse',
            fields={
                'access': serializers.CharField(),
                'refresh': serializers.CharField(),
            }
        ),
        401: OpenApiResponse(
            description="Credenciais inválidas",
            response=inline_serializer(
                name='LoginError',
                fields={
                    'detail': serializers.CharField(),
                }
            )
        )
    }
)
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response(
                {'detail': 'Por favor forneça usuário e senha.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if user is None:
            # Verificar se o usuário existe
            user_exists = User.objects.filter(username=username).exists()
            if not user_exists:
                return Response(
                    {'detail': 'Usuário inválido.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            else:
                return Response(
                    {'detail': 'Senha inválida.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        if not user.is_active:
            return Response(
                {'detail': 'Conta desativada.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Verificar se a conta está bloqueada
        if getattr(user, 'is_locked', False):
            return Response(
                {'detail': 'Conta bloqueada. Entre em contato com o administrador.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Gerar tokens
        try:
            tokens = get_tokens_for_user(user)
            
            # Verificar se os tokens gerados estão na blacklist (improvável, mas possível)
            max_attempts = 5
            attempt = 0
            
            while attempt < max_attempts:
                blacklisted_access = BlacklistedTokens.objects.filter(token=tokens["access"]).exists()
                blacklisted_refresh = BlacklistedTokens.objects.filter(token=tokens["refresh"]).exists()
                
                if not blacklisted_access and not blacklisted_refresh:
                    break
                
                # Se tokens estão na blacklist, gerar novos
                logger.warning(f"Tokens gerados estão na blacklist para usuário {getattr(user, 'username', 'desconhecido')}, gerando novos...")
                tokens = get_tokens_for_user(user)
                attempt += 1
            
            if attempt >= max_attempts:
                logger.error(f"Não foi possível gerar tokens válidos para usuário {getattr(user, 'username', 'desconhecido')}")
                return Response(
                    {'detail': 'Erro interno. Tente novamente em alguns minutos.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Resetar tentativas de login falhadas se o método existir
            if hasattr(user, 'reset_failed_login') and callable(getattr(user, 'reset_failed_login')):
                try:
                    reset_method = getattr(user, 'reset_failed_login')
                    reset_method()
                    logger.info(f"Tentativas de login falhadas resetadas para usuário {getattr(user, 'username', 'desconhecido')}")
                except Exception as e:
                    logger.warning(f"Erro ao resetar tentativas de login para usuário {getattr(user, 'username', 'desconhecido')}: {str(e)}")
            else:
                # Resetar manualmente se o método não existir
                try:
                    if hasattr(user, 'failed_login_attempts'):
                        setattr(user, 'failed_login_attempts', 0)
                    if hasattr(user, 'is_locked'):
                        setattr(user, 'is_locked', False)
                    user.save()
                    logger.info(f"Tentativas de login falhadas resetadas manualmente para usuário {getattr(user, 'username', 'desconhecido')}")
                except Exception as e:
                    logger.warning(f"Erro ao resetar tentativas de login manualmente para usuário {getattr(user, 'username', 'desconhecido')}: {str(e)}")

            logger.info(f"Login bem-sucedido para usuário {getattr(user, 'username', 'desconhecido')}")
            return Response(tokens, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Erro ao gerar tokens para usuário {getattr(user, 'username')}: {str(e)}")
            return Response(
                {'detail': 'Erro interno no servidor.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    tags=['Autenticação'],
    summary="Logout de usuário",
    description='''
    Realiza o logout do usuário invalidando os tokens de acesso e refresh.
    
    O token fornecido será adicionado à blacklist para garantir que não possa ser usado novamente.
    ''',
    request=inline_serializer(
        name='LogoutRequest',
        fields={
            'refresh': serializers.CharField(help_text="Token de refresh para invalidar")
        }
    ),
    responses={
        200: LogoutResponseSerializer,
        400: OpenApiResponse(
            description="Token inválido ou ausente",
            response=inline_serializer(
                name='LogoutError',
                fields={
                    'detail': serializers.CharField(),
                }
            )
        )
    }
)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh') if isinstance(request.data, dict) else None
            if not refresh_token:
                return Response(
                    {'detail': 'Token de refresh é obrigatório.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Adicionar o token de refresh na blacklist
            BlacklistedTokens.objects.get_or_create(
                token=refresh_token,
                defaults={'user': request.user}
            )

            # Também adicionar o token de acesso na blacklist se disponível
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if auth_header:
                try:
                    token_parts = auth_header.split()
                    if len(token_parts) == 2 and token_parts[0] in ('Bearer', 'JWT'):
                        access_token = token_parts[1]
                        BlacklistedTokens.objects.get_or_create(
                            token=access_token,
                            defaults={'user': request.user}
                        )
                except Exception as e:
                    logger.warning(f"Erro ao blacklistar token de acesso: {str(e)}")

            logger.info(f"Logout realizado para usuário {getattr(request.user, 'username', 'desconhecido')}")
            return Response(
                {'message': 'Logout realizado com sucesso.'},
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"Erro durante logout: {str(e)}")
            return Response(
                {'detail': 'Erro interno no servidor durante logout.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    tags=['Autenticação'],
    summary="Refresh de token de acesso",
    description='''
    Gera um novo token de acesso usando o token de refresh.
    
    Use este endpoint quando o token de acesso expirar.
    ''',
    request=inline_serializer(
        name='RefreshRequest',
        fields={
            'refresh': serializers.CharField()
        }
    ),
    responses={
        200: inline_serializer(
            name='RefreshResponse',
            fields={
                'access': serializers.CharField(),
            }
        ),
        401: OpenApiResponse(
            description="Token de refresh inválido ou expirado",
            response=inline_serializer(
                name='RefreshError',
                fields={
                    'detail': serializers.CharField(),
                }
            )
        )
    }
)
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh') if isinstance(request.data, dict) else None
            if not refresh_token:
                return Response(
                    {'detail': 'Token de refresh é obrigatório.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Verificar se o token está na blacklist
            if BlacklistedTokens.objects.filter(token=refresh_token).exists():
                logger.warning("Tentativa de usar token de refresh blacklisted")
                return Response(
                    {'detail': 'Token de refresh foi invalidado.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Chamar o método original
            response = super().post(request, *args, **kwargs)
            
            if response.status_code == 200:
                logger.info("Token de acesso renovado com sucesso")
            
            return response
            
        except Exception as e:
            logger.error(f"Erro durante refresh de token: {str(e)}")
            return Response(
                {'detail': 'Erro interno no servidor durante refresh de token.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
