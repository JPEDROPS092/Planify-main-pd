from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, OpenApiExample
from .authentication import get_tokens_for_user
from .serializers import LogoutResponseSerializer

@extend_schema(
    tags=['Autenticação'],
    summary="Login de usuário",
    description='''
    Realiza o login do usuário e retorna os tokens de acesso e refresh.
    
    O token de acesso deve ser usado no header de todas as requisições:
    `Authorization: JWT <access_token>`
    
    Quando o token de acesso expirar (após 1 hora), use o token de refresh para obter um novo.
    ''',
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'username': {
                    'type': 'string',
                    'description': 'Nome de usuário'
                },
                'password': {
                    'type': 'string',
                    'description': 'Senha do usuário',
                    'format': 'password'
                }
            },
            'required': ['username', 'password']
        }
    },
    responses={
        200: {
            'type': 'object',
            'properties': {
                'access': {
                    'type': 'string',
                    'description': 'Token de acesso JWT (expira em 1 hora)'
                },
                'refresh': {
                    'type': 'string',
                    'description': 'Token de refresh JWT (expira em 7 dias)'
                }
            }
        },
        401: {
            'type': 'object',
            'properties': {
                'detail': {
                    'type': 'string',
                    'example': 'Credenciais inválidas.'
                }
            }
        }
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

        tokens = get_tokens_for_user(user)
        return Response(tokens, status=status.HTTP_200_OK)

@extend_schema(
    tags=['Autenticação'],
    summary="Atualizar token de acesso",
    description='''
    Atualiza um token de acesso expirado usando o token de refresh.
    
    Envie o token de refresh para obter um novo token de acesso.
    Se o token de refresh também estiver expirado (após 7 dias), será necessário fazer login novamente.
    ''',
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'refresh': {
                    'type': 'string',
                    'description': 'Token de refresh JWT'
                }
            },
            'required': ['refresh']
        }
    },
    responses={
        200: {
            'type': 'object',
            'properties': {
                'access': {
                    'type': 'string',
                    'description': 'Novo token de acesso JWT'
                }
            }
        },
        401: {
            'type': 'object',
            'properties': {
                'detail': {
                    'type': 'string',
                    'example': 'Token inválido ou expirado.'
                }
            }
        }
    }
)
class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
    authentication_classes = []  # Remove todas as autenticações para o refresh

@extend_schema(
    tags=['Autenticação'],
    summary="Logout de usuário",
    description='''
    Realiza o logout do usuário invalidando o token atual.
    
    Após o logout, o token de acesso não poderá mais ser usado.
    É recomendado também descartar o token de refresh no cliente.
    ''',
    responses={
        200: LogoutResponseSerializer,
        400: LogoutResponseSerializer,
    }
)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutResponseSerializer

    def post(self, request):
        try:
            request.auth.delete()
            return Response(
                {"message": "Logout realizado com sucesso"}, 
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {"message": "Erro ao realizar logout"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
