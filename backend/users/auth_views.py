from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, inline_serializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from .authentication import get_tokens_for_user
from .serializers import LogoutResponseSerializer
from .models import BlacklistedTokens
import logging

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
            return Response(
                {'detail': 'Credenciais inválidas.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {'detail': 'Conta desativada.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Verificar se a conta está bloqueada
        if hasattr(user, 'is_locked') and user.is_locked:
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
                logger.warning(f"Tokens gerados estão na blacklist para usuário {user.username}, gerando novos...")
                tokens = get_tokens_for_user(user)
                attempt += 1
            
            if attempt >= max_attempts:
                logger.error(f"Não foi possível gerar tokens válidos para usuário {user.username}")
                return Response(
                    {'detail': 'Erro interno. Tente novamente em alguns minutos.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Resetar tentativas de login falhadas
            if hasattr(user, 'reset_failed_login'):
                user.reset_failed_login()

            logger.info(f"Login bem-sucedido para usuário {user.username}")
            return Response(tokens, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Erro ao gerar tokens para usuário {user.username}: {str(e)}")
            return Response(
                {'detail': 'Erro interno no servidor.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    tags=['Autenticação'],
    summary="Atualizar token de acesso",
    description='''
    Atualiza um token de acesso expirado usando o token de refresh.
    ''',
    request=inline_serializer(
        name='RefreshRequest',
        fields={
            'refresh': serializers.CharField(),
        }
    ),
    responses={
        200: inline_serializer(
            name='RefreshResponse',
            fields={
                'access': serializers.CharField(),
            }
        ),
    }
)
class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
    authentication_classes = []


@extend_schema(
    tags=['Autenticação'],
    summary="Logout de usuário",
    description='Realiza o logout do usuário invalidando o token atual.',
    responses={
        200: LogoutResponseSerializer,
    }
)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutResponseSerializer

    def post(self, request):
        try:
            # Obter o token do header de autorização
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header:
                # Extrair o token (formato: "Bearer <token>" ou "JWT <token>")
                token_parts = auth_header.split()
                if len(token_parts) == 2:
                    token = token_parts[1]
                    
                    # Adicionar token à blacklist
                    BlacklistedTokens.objects.get_or_create(token=token)
                    
                    logger.info(f"Logout realizado com sucesso para usuário {request.user.username}")
                    return Response(
                        {"message": "Logout realizado com sucesso"}, 
                        status=status.HTTP_200_OK
                    )
            
            return Response(
                {"message": "Token não encontrado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            logger.error(f"Erro ao realizar logout: {str(e)}")
            return Response(
                {"message": "Erro ao realizar logout", "detail": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
