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

@extend_schema(
    tags=['Autenticação'],
    summary="Login de usuário",
    description='''
    Realiza o login do usuário e retorna os tokens de acesso e refresh.
    
    O token de acesso deve ser usado no header de todas as requisições:
    `Authorization: JWT <access_token>`
    
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

        tokens = get_tokens_for_user(user)
        return Response(tokens, status=status.HTTP_200_OK)


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
