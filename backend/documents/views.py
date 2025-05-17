from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from core.utils import swagger_schema_with_examples
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
    
    @swagger_schema_with_examples(
        summary="Listar documentos",
        description="Retorna a lista de todos os documentos com filtros opcionais.",
        tags=['Documentos'],
        parameters=[
            {
                'name': 'projeto',
                'description': "Filtrar por projeto (ID)",
                'type': 'integer',
                'location': 'query',
                'required': False
            },
            {
                'name': 'tarefa',
                'description': "Filtrar por tarefa (ID)",
                'type': 'integer',
                'location': 'query',
                'required': False
            },
            {
                'name': 'tipo',
                'description': "Filtrar por tipo de documento (REQUISITO, DESIGN, MANUAL, RELATORIO, ATA, OUTRO)",
                'type': 'string',
                'location': 'query',
                'required': False
            },
            {
                'name': 'tipo_arquivo',
                'description': "Filtrar por tipo MIME do arquivo",
                'type': 'string',
                'location': 'query',
                'required': False
            },
            {
                'name': 'texto',
                'description': "Buscar por texto no título ou descrição",
                'type': 'string',
                'location': 'query',
                'required': False
            },
        ],
        responses={
            '200': {
                'description': 'Lista de documentos recuperada com sucesso'
            }
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_schema_with_examples(
        summary="Criar documento",
        description="Cria um novo documento no sistema.",
        tags=['Documentos'],
        responses={
            '201': {
                'description': 'Documento criado com sucesso',
                'examples': [
                    {
                        'name': 'exemplo_documento',
                        'value': {
                            'id': 1,
                            'titulo': 'Manual do Usuário',
                            'descricao': 'Manual de instruções para o sistema',
                            'tipo': 'MANUAL',
                            'arquivo': 'documentos/manual.pdf',
                            'tipo_arquivo': 'application/pdf',
                            'tamanho_arquivo': 1024,
                            'projeto': 1,
                            'tarefa': 2,
                            'enviado_por': 1,
                            'data_upload': '2023-01-01T10:00:00Z'
                        }
                    }
                ]
            },
            '400': {
                'description': 'Dados inválidos'
            }
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_schema_with_examples(
        summary="Obter documento",
        description="Retorna os detalhes de um documento específico.",
        tags=['Documentos'],
        responses={
            '200': {
                'description': 'Detalhes do documento recuperados com sucesso'
            },
            '404': {
                'description': 'Documento não encontrado'
            }
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_schema_with_examples(
        summary="Atualizar documento",
        description="Atualiza todos os campos de um documento existente.",
        tags=['Documentos'],
        responses={
            '200': {
                'description': 'Documento atualizado com sucesso'
            },
            '400': {
                'description': 'Dados inválidos'
            },
            '404': {
                'description': 'Documento não encontrado'
            }
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_schema_with_examples(
        summary="Atualizar documento parcialmente",
        description="Atualiza parcialmente um documento existente.",
        tags=['Documentos'],
        responses={
            '200': {
                'description': 'Documento atualizado parcialmente com sucesso'
            },
            '400': {
                'description': 'Dados inválidos'
            },
            '404': {
                'description': 'Documento não encontrado'
            }
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_schema_with_examples(
        summary="Excluir documento",
        description="Remove um documento do sistema.",
        tags=['Documentos'],
        responses={
            '204': {
                'description': 'Documento excluído com sucesso'
            },
            '404': {
                'description': 'Documento não encontrado'
            }
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
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
    
    @swagger_schema_with_examples(
        summary="Histórico do documento",
        description="Retorna o histórico de versões do documento.",
        tags=['Documentos'],
        responses={
            '200': {
                'description': 'Histórico de versões recuperado com sucesso'
            },
            '404': {
                'description': 'Documento não encontrado'
            }
        }
    )
    @action(detail=True, methods=['get'])
    def historico(self, request, pk=None):
        """
        Retorna o histórico de versões do documento.
        """
        documento = self.get_object()
        historico = documento.historico.all()
        serializer = HistoricoDocumentoSerializer(historico, many=True)
        return Response(serializer.data)
    
    @swagger_schema_with_examples(
        summary="Adicionar comentário",
        description="Adiciona um comentário ao documento.",
        tags=['Documentos'],
        examples={
            'exemplo_comentario': {
                'value': {
                    'texto': 'Este documento precisa de revisão na seção 3.'
                },
                'summary': 'Exemplo de comentário',
                'description': 'Exemplo de como adicionar um comentário ao documento'
            }
        },
        responses={
            '201': {
                'description': 'Comentário adicionado com sucesso'
            },
            '400': {
                'description': 'Dados inválidos'
            },
            '404': {
                'description': 'Documento não encontrado'
            }
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
    
    @swagger_schema_with_examples(
        summary="Associar tarefa",
        description="Associa o documento a uma tarefa.",
        tags=['Documentos'],
        examples={
            'exemplo_associacao': {
                'value': {
                    'tarefa_id': 1
                },
                'summary': 'Exemplo de associação',
                'description': 'Exemplo de como associar um documento a uma tarefa'
            },
            'exemplo_remocao': {
                'value': {
                    'tarefa_id': 0
                },
                'summary': 'Exemplo de remoção',
                'description': 'Exemplo de como remover a associação de um documento com uma tarefa'
            }
        },
        responses={
            '200': {
                'description': 'Documento associado/desassociado com sucesso'
            },
            '400': {
                'description': 'Dados inválidos'
            },
            '404': {
                'description': 'Documento não encontrado'
            }
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
    filterset_fields = ['documento', 'alterado_por']
    
    @swagger_schema_with_examples(
        summary="Listar histórico de documentos",
        description="Retorna a lista de todo o histórico de documentos.",
        tags=['Histórico de Documentos'],
        parameters=[
            {
                'name': 'documento',
                'description': "Filtrar por documento (ID)",
                'type': 'integer',
                'location': 'query',
                'required': False
            },
            {
                'name': 'alterado_por',
                'description': "Filtrar por usuário que alterou (ID)",
                'type': 'integer',
                'location': 'query',
                'required': False
            },
        ],
        responses={
            '200': {
                'description': 'Lista de histórico de documentos recuperada com sucesso'
            }
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_schema_with_examples(
        summary="Detalhes do histórico",
        description="Retorna os detalhes de um registro específico do histórico.",
        tags=['Histórico de Documentos'],
        responses={
            '200': {
                'description': 'Detalhes do registro de histórico recuperados com sucesso'
            },
            '404': {
                'description': 'Registro de histórico não encontrado'
            }
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
    filterset_fields = ['documento', 'autor']
    ordering_fields = ['criado_em']
    
    @swagger_schema_with_examples(
        summary="Listar comentários",
        description="Retorna a lista de todos os comentários.",
        tags=['Comentários'],
        parameters=[
            {
                'name': 'documento',
                'description': "Filtrar por documento (ID)",
                'type': 'integer',
                'location': 'query',
                'required': False
            },
            {
                'name': 'autor',
                'description': "Filtrar por autor (ID)",
                'type': 'integer',
                'location': 'query',
                'required': False
            },
        ],
        responses={
            '200': {
                'description': 'Lista de comentários recuperada com sucesso'
            }
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_schema_with_examples(
        summary="Criar comentário",
        description="Cria um novo comentário para um documento.",
        tags=['Comentários'],
        examples={
            'exemplo_comentario': {
                'value': {
                    'documento': 1,
                    'texto': 'Este documento está muito bem estruturado.'
                },
                'summary': 'Exemplo de comentário',
                'description': 'Exemplo de como criar um comentário para um documento'
            }
        },
        responses={
            '201': {
                'description': 'Comentário criado com sucesso'
            },
            '400': {
                'description': 'Dados inválidos'
            }
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_schema_with_examples(
        summary="Detalhes do comentário",
        description="Retorna os detalhes de um comentário específico.",
        tags=['Comentários'],
        responses={
            '200': {
                'description': 'Detalhes do comentário recuperados com sucesso'
            },
            '404': {
                'description': 'Comentário não encontrado'
            }
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_schema_with_examples(
        summary="Atualizar comentário",
        description="Atualiza um comentário existente.",
        tags=['Comentários'],
        examples={
            'exemplo_atualizacao': {
                'value': {
                    'texto': 'Texto atualizado do comentário.'
                },
                'summary': 'Exemplo de atualização',
                'description': 'Exemplo de como atualizar um comentário'
            }
        },
        responses={
            '200': {
                'description': 'Comentário atualizado com sucesso'
            },
            '400': {
                'description': 'Dados inválidos'
            },
            '404': {
                'description': 'Comentário não encontrado'
            }
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_schema_with_examples(
        summary="Atualizar comentário parcialmente",
        description="Atualiza parcialmente um comentário existente.",
        tags=['Comentários'],
        examples={
            'exemplo_atualizacao_parcial': {
                'value': {
                    'texto': 'Atualização parcial do texto.'
                },
                'summary': 'Exemplo de atualização parcial',
                'description': 'Exemplo de como atualizar parcialmente um comentário'
            }
        },
        responses={
            '200': {
                'description': 'Comentário atualizado parcialmente com sucesso'
            },
            '400': {
                'description': 'Dados inválidos'
            },
            '404': {
                'description': 'Comentário não encontrado'
            }
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_schema_with_examples(
        summary="Excluir comentário",
        description="Remove um comentário do sistema.",
        tags=['Comentários'],
        responses={
            '204': {
                'description': 'Comentário excluído com sucesso'
            },
            '404': {
                'description': 'Comentário não encontrado'
            }
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)
