from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import UserProfile
from .serializers import UserCreateSerializer
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    """
    View para registro público de usuários.
    Permite que qualquer pessoa crie uma conta sem necessidade de autenticação prévia.
    """
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Definir o papel padrão como TEAM_MEMBER se não for especificado
            if 'role' not in serializer.validated_data:
                serializer.validated_data['role'] = 'TEAM_MEMBER'
                
            # Criar o usuário
            user = serializer.save()
            logger.info(f"Novo usuário registrado: {user.username} (ID: {user.id})")
            
            # Criar perfil de usuário automaticamente
            UserProfile.objects.create(user=user)
            logger.info(f"Perfil criado para o usuário: {user.username}")
            
            # Retornar resposta de sucesso
            return Response({
                'detail': 'Usuário registrado com sucesso',
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
