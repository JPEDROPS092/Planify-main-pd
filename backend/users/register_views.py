from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework import serializers
from .models import UserProfile
from .serializers import UserCreateSerializer
import logging

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
