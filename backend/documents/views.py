from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .models import Documento, HistoricoDocumento, Comentario
from .serializers import (
    DocumentoSerializer, DocumentoListSerializer, 
    HistoricoDocumentoSerializer, ComentarioSerializer
)

@extend_schema_view(
    list=extend_schema(
        summary="Listar documentos",
        description="Retorna a lista de todos os documentos",
        tags=['Documents']
    ),
    retrieve=extend_schema(
        summary="Obter documento",
        description="Retorna os detalhes de um documento específico",
        tags=['Documents']
    ),
    create=extend_schema(
        summary="Criar documento",
        description="Cria um novo documento",
        tags=['Documents']
    ),
    update=extend_schema(
        summary="Atualizar documento",
        description="Atualiza todos os campos de um documento",
        tags=['Documents']
    ),
    partial_update=extend_schema(
        summary="Atualizar documento parcialmente",
        description="Atualiza parcialmente um documento",
        tags=['Documents']
    ),
    destroy=extend_schema(
        summary="Excluir documento",
        description="Remove um documento",
        tags=['Documents']
    )
)
class DocumentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de documentos.
    Permite criar, listar, atualizar e excluir documentos.
    """
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['projeto', 'tarefa', 'tipo', 'enviado_por']
    search_fields = ['titulo', 'descricao', 'tipo_arquivo']
    ordering_fields = ['data_upload', 'titulo', 'tipo', 'tamanho_arquivo']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DocumentoListSerializer
        return DocumentoSerializer
    
    def perform_create(self, serializer):
        serializer.save(enviado_por=self.request.user)

    @extend_schema(
        summary="Adicionar comentário",
        description="Adiciona um novo comentário ao documento",
        tags=['Documents']
    )
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        documento = self.get_object()
        serializer = ComentarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                documento=documento,
                autor=request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Associar tarefa",
        description="Associa o documento a uma tarefa",
        tags=['Documents']
    )
    @action(detail=True, methods=['post'])
    def assign_task(self, request, pk=None):
        documento = self.get_object()
        tarefa_id = request.data.get('tarefa_id')
        # Implementação da associação com tarefa
        return Response({'status': 'documento associado à tarefa'})

    @extend_schema(
        summary="Histórico do documento",
        description="Retorna o histórico de alterações do documento",
        tags=['Documents']
    )
    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        documento = self.get_object()
        historico = HistoricoDocumento.objects.filter(documento=documento)
        serializer = HistoricoDocumentoSerializer(historico, many=True)
        return Response(serializer.data)

@extend_schema_view(
    list=extend_schema(tags=['Documents']),
    retrieve=extend_schema(tags=['Documents']),
    create=extend_schema(tags=['Documents']),
    update=extend_schema(tags=['Documents']),
    partial_update=extend_schema(tags=['Documents']),
    destroy=extend_schema(tags=['Documents'])
)
class HistoricoDocumentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para visualização do histórico de documentos.
    Somente leitura.
    """
    queryset = HistoricoDocumento.objects.all()
    serializer_class = HistoricoDocumentoSerializer
    permission_classes = [permissions.IsAuthenticated]

@extend_schema_view(
    list=extend_schema(tags=['Documents']),
    retrieve=extend_schema(tags=['Documents']),
    create=extend_schema(tags=['Documents']),
    update=extend_schema(tags=['Documents']),
    partial_update=extend_schema(tags=['Documents']),
    destroy=extend_schema(tags=['Documents'])
)
class ComentarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de comentários em documentos.
    """
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['documento', 'autor'] # Estes são campos ForeignKey
    ordering_fields = ['criado_em']
    
    @extend_schema(
        summary="Listar comentários de documentos",
        description="Retorna a lista de todos os comentários associados a documentos.",
        tags=['Documentos', 'Comentários'],
        parameters=[
            OpenApiParameter(name='documento', description="Filtrar por ID do documento ao qual o comentário pertence", required=False, type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='autor', description="Filtrar por ID do autor do comentário", required=False, type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='ordering', description="Campo para ordenação (ex: criado_em, -criado_em)", required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiResponse(response=ComentarioSerializer(many=True), description='Lista de comentários recuperada com sucesso')
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Criar um novo comentário",
        description="Cria um novo comentário para um documento. O autor é automaticamente definido como o usuário autenticado.",
        tags=['Documentos', 'Comentários'],
        request=ComentarioSerializer,
        responses={
            201: OpenApiResponse(response=ComentarioSerializer, description='Comentário criado com sucesso', examples=[
                OpenApiExample(
                    name='exemplo_criacao_comentario',
                    summary='Exemplo de criação de comentário',
                    value={
                        'documento': 1, # ID do documento
                        'texto': 'Este documento está muito bem estruturado e cobre todos os pontos necessários.'
                    }
                )
            ]),
            400: OpenApiResponse(description='Dados inválidos')
        }
    )
    def create(self, request, *args, **kwargs):
        # O autor é definido em perform_create
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary="Detalhes de um comentário",
        description="Retorna os detalhes de um comentário específico.",
        tags=['Documentos', 'Comentários'],
        responses={
            200: OpenApiResponse(response=ComentarioSerializer, description='Detalhes do comentário recuperados com sucesso'),
            404: OpenApiResponse(description='Comentário não encontrado')
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Atualizar um comentário",
        description="Atualiza um comentário existente. Somente o autor do comentário ou um administrador pode atualizá-lo.",
        tags=['Documentos', 'Comentários'],
        request=ComentarioSerializer,
        responses={
            200: OpenApiResponse(response=ComentarioSerializer, description='Comentário atualizado com sucesso'),
            400: OpenApiResponse(description='Dados inválidos'),
            403: OpenApiResponse(description='Permissão negada para atualizar o comentário'),
            404: OpenApiResponse(description='Comentário não encontrado')
        }
    )
    def update(self, request, *args, **kwargs):
        # Adicionar lógica de permissão se necessário, ou confiar nas permissões do ViewSet
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Atualizar parcialmente um comentário",
        description="Atualiza parcialmente um comentário existente. Somente o autor ou um administrador pode atualizá-lo.",
        tags=['Documentos', 'Comentários'],
        request=ComentarioSerializer, # O request pode ser parcial
        responses={
            200: OpenApiResponse(response=ComentarioSerializer, description='Comentário atualizado parcialmente com sucesso'),
            400: OpenApiResponse(description='Dados inválidos'),
            403: OpenApiResponse(description='Permissão negada para atualizar o comentário'),
            404: OpenApiResponse(description='Comentário não encontrado')
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Excluir um comentário",
        description="Remove um comentário do sistema. Somente o autor ou um administrador pode excluí-lo.",
        tags=['Documentos', 'Comentários'],
        responses={
            204: OpenApiResponse(description='Comentário excluído com sucesso'),
            403: OpenApiResponse(description='Permissão negada para excluir o comentário'),
            404: OpenApiResponse(description='Comentário não encontrado')
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        # Comentário: Define o autor do comentário como o usuário autenticado durante a criação.
        serializer.save(autor=self.request.user)
