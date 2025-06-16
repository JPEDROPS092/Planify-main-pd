from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Equipe, MembroEquipe, PermissaoEquipe
from .serializers import (
    EquipeSerializer, EquipeListSerializer, MembroEquipeSerializer, 
    PermissaoEquipeSerializer, UserMinimalSerializer
)

User = get_user_model()

@extend_schema_view(
    list=extend_schema(
        summary="Listar equipes",
        tags=["Equipes"],
        description="Retorna uma lista paginada de equipes.",
        parameters=[
            OpenApiParameter(name='texto', description='Filtrar por nome ou descrição', required=False, type=str),
            OpenApiParameter(name='minhas_equipes', description='Filtrar apenas minhas equipes', required=False, type=bool),
            OpenApiParameter(name='usuario', description='Filtrar por membro da equipe', required=False, type=int),
        ],
        responses={200: EquipeListSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Obter detalhes da equipe",
        tags=["Equipes"],
        description="Retorna informações detalhadas de uma equipe específica.",
        responses={200: EquipeSerializer}
    ),
    create=extend_schema(
        summary="Criar nova equipe",
        tags=["Equipes"],
        description="Cria uma nova equipe.",
        responses={201: EquipeSerializer}
    ),
    update=extend_schema(
        summary="Atualizar equipe",
        tags=["Equipes"],
        description="Atualiza todos os campos de uma equipe existente.",
        responses={200: EquipeSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualizar equipe parcialmente",
        tags=["Equipes"],
        description="Atualiza parcialmente uma equipe existente.",
        responses={200: EquipeSerializer}
    ),
    destroy=extend_schema(
        summary="Excluir equipe",
        tags=["Equipes"],
        description="Remove uma equipe existente.",
        responses={204: None}
    )
)
class EquipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de equipes.
    Permite criar, listar, atualizar e excluir equipes.
    """
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'criado_em']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EquipeListSerializer
        return EquipeSerializer
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)
    
    def get_queryset(self):
        """
        Filtra equipes com base nos parâmetros da URL e permissões do usuário.
        """
        queryset = Equipe.objects.all()
        
        # Filtra por membro
        usuario_id = self.request.GET.get('usuario')
        if usuario_id:
            queryset = queryset.filter(membros__usuario__id=usuario_id)
        
        # Filtra minhas equipes
        minhas_equipes = self.request.GET.get('minhas_equipes')
        if minhas_equipes and minhas_equipes.lower() == 'true':
            queryset = queryset.filter(membros__usuario=self.request.user)
        
        # Filtra por texto (busca em nome e descrição)
        texto = self.request.GET.get('texto')
        if texto:
            queryset = queryset.filter(
                Q(nome__icontains=texto) | Q(descricao__icontains=texto)
            )
        
        return queryset.distinct()
    
    @extend_schema(
        summary="Listar membros da equipe",
        tags=["Equipes"],
        description="Retorna a lista de membros de uma equipe específica.",
        responses={200: MembroEquipeSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def membros(self, request, pk=None):
        """
        Retorna a lista de membros da equipe.
        """
        equipe = self.get_object()
        membros = equipe.membros.all()
        serializer = MembroEquipeSerializer(membros, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Adicionar membro à equipe",
        tags=["Equipes"],
        description="Adiciona um novo membro à equipe.",
        request=MembroEquipeSerializer,
        responses={201: MembroEquipeSerializer}
    )
    @action(detail=True, methods=['post'])
    def adicionar_membro(self, request, pk=None):
        """
        Adiciona um membro à equipe.
        """
        equipe = self.get_object()
        serializer = MembroEquipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(equipe=equipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Atualizar papel do membro",
        tags=["Equipes"],
        description="Atualiza o papel de um membro na equipe.",
        request=MembroEquipeSerializer,
        responses={200: MembroEquipeSerializer}
    )
    @action(detail=True, methods=['post'])
    def atualizar_papel_membro(self, request, pk=None):
        """
        Atualiza o papel de um membro da equipe.
        """
        equipe = self.get_object()
        membro = equipe.membros.get(usuario_id=request.data.get('usuario'))
        serializer = MembroEquipeSerializer(membro, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Remover membro da equipe",
        tags=["Equipes"],
        description="Remove um membro da equipe.",
        responses={204: None}
    )
    @action(detail=True, methods=['post'])
    def remover_membro(self, request, pk=None):
        """
        Remove um membro da equipe.
        """
        equipe = self.get_object()
        membro = equipe.membros.get(usuario_id=request.data.get('usuario'))
        membro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Retornar usuários disponíveis à equipe",
        tags=["Equipes"],
        description="Retorna a lista de usuários que podem ser adicionados à equipe.",
        responses={200: UserMinimalSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def usuarios_disponiveis(self, request):
        """
        Retorna a lista de usuários disponíveis para adicionar a uma equipe.
        """
        equipe_id = request.query_params.get('equipe')
        usuarios = User.objects.exclude(membros_equipe__equipe_id=equipe_id)
        serializer = UserMinimalSerializer(usuarios, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="Listar permissões de equipe",
        tags=["Permissões de Equipe"],
        description="Retorna uma lista de permissões de equipe.",
        responses={200: PermissaoEquipeSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Obter detalhes da permissão",
        tags=["Permissões de Equipe"],
        description="Retorna detalhes de uma permissão específica.",
        responses={200: PermissaoEquipeSerializer}
    ),
    create=extend_schema(
        summary="Criar permissão",
        tags=["Permissões de Equipe"],
        description="Cria uma nova permissão de equipe.",
        responses={201: PermissaoEquipeSerializer}
    ),
    update=extend_schema(
        summary="Atualizar permissão",
        tags=["Permissões de Equipe"],
        description="Atualiza uma permissão de equipe existente.",
        responses={200: PermissaoEquipeSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualizar permissão parcialmente",
        tags=["Permissões de Equipe"],
        description="Atualiza parcialmente uma permissão de equipe.",
        responses={200: PermissaoEquipeSerializer}
    ),
    destroy=extend_schema(
        summary="Excluir permissão",
        tags=["Permissões de Equipe"],
        description="Remove uma permissão de equipe.",
        responses={204: None}
    )
)
class PermissaoEquipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de permissões de equipe.
    """
    queryset = PermissaoEquipe.objects.all()
    serializer_class = PermissaoEquipeSerializer
    permission_classes = [permissions.IsAuthenticated]
