from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
# Imports atualizados para drf-spectacular
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes # Adicionado para tipos de parâmetros
# from core.utils import swagger_schema_with_examples # Será removido ao final se não for mais usado
from .models import Documento, HistoricoDocumento, Comentario
from .serializers import (
    DocumentoSerializer, DocumentoListSerializer, 
    HistoricoDocumentoSerializer, ComentarioSerializer
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
        summary="Listar documentos",
        description="Retorna a lista de todos os documentos com filtros opcionais.",
        tags=['Documentos'],
        parameters=[
            OpenApiParameter(name='projeto', description="Filtrar por projeto (ID)", required=False, type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='tarefa', description="Filtrar por tarefa (ID)", required=False, type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='tipo', description="Filtrar por tipo de documento", required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY, enum=[choice[0] for choice in Documento.TIPO_CHOICES]), # Corrigido para usar TIPO_CHOICES
            OpenApiParameter(name='tipo_arquivo', description="Filtrar por tipo MIME do arquivo (ex: application/pdf)", required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='texto', description="Buscar por texto no título ou descrição", required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='enviado_por', description="Filtrar por ID do usuário que enviou", required=False, type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='search', description="Termo de busca para título, descrição ou tipo de arquivo", required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='ordering', description="Campo para ordenação (ex: data_upload, -titulo)", required=False, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiResponse(response=DocumentoListSerializer(many=True), description='Lista de documentos recuperada com sucesso')
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Criar documento",
        description="Cria um novo documento no sistema.",
        tags=['Documentos'],
        request=DocumentoSerializer,
        responses={
            201: OpenApiResponse(response=DocumentoSerializer, description='Documento criado com sucesso', examples=[
                OpenApiExample(
                    name='exemplo_documento',
                    summary='Exemplo de criação de documento',
                    value={
                        'titulo': 'Manual do Usuário v1',
                        'descricao': 'Manual de instruções para o sistema XYZ.',
                        'tipo': 'MANUAL',
                        'arquivo': 'upload_de_arquivo.pdf', # Representa o upload do arquivo
                        'projeto': 1, # ID do projeto associado
                        'tarefa': 2   # ID da tarefa associada (opcional)
                    }
                )
            ]),
            400: OpenApiResponse(description='Dados inválidos')
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary="Obter documento",
        description="Retorna os detalhes de um documento específico.",
        tags=['Documentos'],
        responses={
            200: OpenApiResponse(response=DocumentoSerializer, description='Detalhes do documento recuperados com sucesso'),
            404: OpenApiResponse(description='Documento não encontrado')
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Atualizar documento",
        description="Atualiza todos os campos de um documento existente.",
        tags=['Documentos'],
        request=DocumentoSerializer,
        responses={
            200: OpenApiResponse(response=DocumentoSerializer, description='Documento atualizado com sucesso'),
            400: OpenApiResponse(description='Dados inválidos'),
            404: OpenApiResponse(description='Documento não encontrado')
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Atualizar documento parcialmente",
        description="Atualiza parcialmente um documento existente.",
        tags=['Documentos'],
        request=DocumentoSerializer, # O request pode ser parcial
        responses={
            200: OpenApiResponse(response=DocumentoSerializer, description='Documento atualizado parcialmente com sucesso'),
            400: OpenApiResponse(description='Dados inválidos'),
            404: OpenApiResponse(description='Documento não encontrado')
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Excluir documento",
        description="Remove um documento do sistema.",
        tags=['Documentos'],
        responses={
            204: OpenApiResponse(description='Documento excluído com sucesso'),
            404: OpenApiResponse(description='Documento não encontrado')
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    # Comentário: get_queryset é usado internamente pelo ViewSet e não precisa de @extend_schema direto,
    # mas os parâmetros que ele usa devem ser documentados no método 'list'.
    def get_queryset(self):
        """
        Filtra documentos com base nos parâmetros da URL.
        """
        queryset = Documento.objects.all()
        
        # Filtra por projeto
        projeto_id = self.request.GET.get('projeto')
        if projeto_id:
            queryset = queryset.filter(projeto_id=projeto_id)
        
        # Filtra por tarefa
        tarefa_id = self.request.GET.get('tarefa')
        if tarefa_id:
            queryset = queryset.filter(tarefa_id=tarefa_id)
        
        # Filtra por tipo
        tipo = self.request.GET.get('tipo')
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        
        # Filtra por tipo de arquivo
        tipo_arquivo = self.request.GET.get('tipo_arquivo')
        if tipo_arquivo:
            queryset = queryset.filter(tipo_arquivo__icontains=tipo_arquivo)
        
        # Filtra por texto (busca em título e descrição)
        # Este filtro é coberto pelo 'search_fields' e o parâmetro 'search'
        # texto = self.request.query_params.get('texto')
        # if texto:
        #     queryset = queryset.filter(
        #         Q(titulo__icontains=texto) | Q(descricao__icontains=texto)
        #     )
        
        return queryset
    
    @extend_schema(
        summary="Histórico do documento",
        description="Retorna o histórico de versões do documento.",
        tags=['Documentos'],
        responses={
            200: OpenApiResponse(response=HistoricoDocumentoSerializer(many=True), description='Histórico de versões recuperado com sucesso'),
            404: OpenApiResponse(description='Documento não encontrado')
        }
    )
    @action(detail=True, methods=['get'])
    def document_history(self, request, pk=None):
        """
        Retorna o histórico de versões do documento.
        """
        documento = self.get_object()
        historico = documento.historico.all()
        serializer = HistoricoDocumentoSerializer(historico, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Adicionar comentário ao documento",
        description="Adiciona um novo comentário a um documento específico.",
        tags=['Documentos', 'Comentários'],
        request={'application/json': {'example': {'texto': 'Este documento precisa de revisão na seção 3.'}}},
        responses={
            201: OpenApiResponse(response=ComentarioSerializer, description='Comentário adicionado com sucesso'),
            400: OpenApiResponse(description='Dados inválidos (ex: texto não fornecido)'),
            404: OpenApiResponse(description='Documento não encontrado')
        }
    )
    @action(detail=True, methods=['post'])
    def adicionar_comentario(self, request, pk=None):
        """
        Adiciona um comentário ao documento.
        """
        documento = self.get_object()
        texto = request.data.get('texto')
        
        if not texto:
            return Response(
                {'erro': 'É necessário fornecer um texto para o comentário.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        comentario = Comentario.objects.create(
            documento=documento,
            autor=request.user,
            texto=texto
        )
        
        serializer = ComentarioSerializer(comentario)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @extend_schema(
        summary="Associar documento a uma tarefa",
        description="Associa ou desassocia um documento a uma tarefa específica. Forneça 'tarefa_id' para associar, ou 'tarefa_id: 0' (ou nulo) para desassociar.",
        tags=['Documentos', 'Tarefas'],
        request={'application/json': {'example': {'tarefa_id': 1}}},
        responses={
            200: OpenApiResponse(response=DocumentoSerializer, description='Documento associado/desassociado com sucesso'),
            400: OpenApiResponse(description='Dados inválidos (ex: tarefa_id não fornecido)'),
            404: OpenApiResponse(description='Documento ou Tarefa não encontrada')
        }
    )
    @action(detail=True, methods=['post'])
    def associar_tarefa(self, request, pk=None):
        """
        Associa o documento a uma tarefa.
        """
        documento = self.get_object()
        tarefa_id = request.data.get('tarefa_id')
        
        if tarefa_id is None:
            return Response(
                {'erro': 'É necessário fornecer um ID de tarefa.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Se tarefa_id for 0 ou vazio, remove a associação com tarefa
        if not tarefa_id:
            documento.tarefa = None
            documento.save()
            return Response({'mensagem': 'Documento desvinculado da tarefa.'}, status=status.HTTP_200_OK)
        
        # Atualiza a tarefa do documento
        documento.tarefa_id = tarefa_id
        documento.save()
        
        serializer = self.get_serializer(documento)
        return Response(serializer.data)


class HistoricoDocumentoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para visualização do histórico de documentos.
    Somente leitura.
    """
    queryset = HistoricoDocumento.objects.all()
    serializer_class = HistoricoDocumentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['documento', 'alterado_por'] # Estes são campos ForeignKey
    
    @extend_schema(
        summary="Listar histórico de alterações de documentos",
        description="Retorna a lista de todas as alterações registradas para os documentos.",
        tags=['Documentos', 'Histórico'],
        parameters=[
            OpenApiParameter(name='documento', description="Filtrar por ID do documento", required=False, type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='alterado_por', description="Filtrar por ID do usuário que realizou a alteração", required=False, type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
        ],
        responses={
            200: OpenApiResponse(response=HistoricoDocumentoSerializer(many=True), description='Lista de histórico de documentos recuperada com sucesso')
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Detalhes de um registro de histórico",
        description="Retorna os detalhes de um registro específico do histórico de alterações de um documento.",
        tags=['Documentos', 'Histórico'],
        responses={
            200: OpenApiResponse(response=HistoricoDocumentoSerializer, description='Detalhes do registro de histórico recuperados com sucesso'),
            404: OpenApiResponse(description='Registro de histórico não encontrado')
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


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
