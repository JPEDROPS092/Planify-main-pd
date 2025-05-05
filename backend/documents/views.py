from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
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
    
    def get_queryset(self):
        """
        Filtra documentos com base nos parâmetros da URL.
        """
        queryset = Documento.objects.all()
        
        # Filtra por projeto
        projeto_id = self.request.query_params.get('projeto')
        if projeto_id:
            queryset = queryset.filter(projeto_id=projeto_id)
        
        # Filtra por tarefa
        tarefa_id = self.request.query_params.get('tarefa')
        if tarefa_id:
            queryset = queryset.filter(tarefa_id=tarefa_id)
        
        # Filtra por tipo
        tipo = self.request.query_params.get('tipo')
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        
        # Filtra por tipo de arquivo
        tipo_arquivo = self.request.query_params.get('tipo_arquivo')
        if tipo_arquivo:
            queryset = queryset.filter(tipo_arquivo__icontains=tipo_arquivo)
        
        # Filtra por texto (busca em título e descrição)
        texto = self.request.query_params.get('texto')
        if texto:
            queryset = queryset.filter(
                Q(titulo__icontains=texto) | Q(descricao__icontains=texto)
            )
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def historico(self, request, pk=None):
        """
        Retorna o histórico de versões do documento.
        """
        documento = self.get_object()
        historico = documento.historico.all()
        serializer = HistoricoDocumentoSerializer(historico, many=True)
        return Response(serializer.data)
    
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
    filterset_fields = ['documento', 'alterado_por']


class ComentarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de comentários em documentos.
    """
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['documento', 'autor']
    ordering_fields = ['criado_em']
    
    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)
