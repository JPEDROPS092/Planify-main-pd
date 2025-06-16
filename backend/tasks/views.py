from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateFromToRangeFilter, CharFilter, BooleanFilter, NumberFilter
from django.db.models import Q, Count, Prefetch, F, ExpressionWrapper, BooleanField, Case, When, Value
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from .models import Tarefa, AtribuicaoTarefa, ComentarioTarefa, HistoricoStatusTarefa
from .serializers import (
    TarefaSerializer, TarefaListSerializer, AtribuicaoTarefaSerializer, 
    ComentarioTarefaSerializer, HistoricoStatusTarefaSerializer
)


class TarefaFilter(FilterSet):
    """
    Filtro personalizado para tarefas.
    
    Permite filtrar tarefas por diversos critérios como data, status, prioridade, etc.
    """
    titulo = CharFilter(lookup_expr='icontains', help_text="Filtra por título (case insensitive)")
    descricao = CharFilter(lookup_expr='icontains', help_text="Filtra por descrição (case insensitive)")
    data_inicio_apos = DateFromToRangeFilter(field_name='data_inicio', lookup_expr='gte', 
                                          help_text="Filtra tarefas com data de início após a data especificada")
    data_inicio_antes = DateFromToRangeFilter(field_name='data_inicio', lookup_expr='lte', 
                                           help_text="Filtra tarefas com data de início antes da data especificada")
    data_termino_apos = DateFromToRangeFilter(field_name='data_termino', lookup_expr='gte', 
                                           help_text="Filtra tarefas com data de término após a data especificada")
    data_termino_antes = DateFromToRangeFilter(field_name='data_termino', lookup_expr='lte', 
                                            help_text="Filtra tarefas com data de término antes da data especificada")
    status = CharFilter(method='filter_status', help_text="Filtra por status (pode ser múltiplos, separados por vírgula)")
    prioridade = CharFilter(method='filter_prioridade', help_text="Filtra por prioridade (pode ser múltiplas, separadas por vírgula)")
    responsavel = CharFilter(method='filter_responsavel', help_text="Filtra tarefas pelo ID do usuário responsável")
    sem_responsavel = BooleanFilter(method='filter_sem_responsavel', help_text="Filtra tarefas sem responsáveis atribuídos")
    atrasada = BooleanFilter(method='filter_atrasada', help_text="Filtra tarefas atrasadas (data_termino < hoje e status != FEITO)")
    minhas_tarefas = BooleanFilter(method='filter_minhas_tarefas', help_text="Filtra tarefas do usuário autenticado")
    sem_sprint = BooleanFilter(method='filter_sem_sprint', help_text="Filtra tarefas que não estão associadas a nenhuma sprint")
    
    class Meta:
        model = Tarefa
        fields = ['titulo', 'descricao', 'projeto', 'sprint', 'status', 'prioridade',
                 'data_inicio_apos', 'data_inicio_antes', 'data_termino_apos', 'data_termino_antes',
                 'responsavel', 'sem_responsavel', 'atrasada', 'minhas_tarefas', 'sem_sprint']
    
    def filter_status(self, queryset, name, value):
        """Filtra por múltiplos status separados por vírgula."""
        if not value:
            return queryset
        status_list = [s.strip().upper() for s in value.split(',')]
        return queryset.filter(status__in=status_list)
    
    def filter_prioridade(self, queryset, name, value):
        """Filtra por múltiplas prioridades separadas por vírgula."""
        if not value:
            return queryset
        prioridade_list = [p.strip().upper() for p in value.split(',')]
        return queryset.filter(prioridade__in=prioridade_list)
    
    def filter_responsavel(self, queryset, name, value):
        """Filtra tarefas pelo usuário responsável."""
        if not value:
            return queryset
        return queryset.filter(atribuicoes__usuario__id=value)
    
    def filter_sem_responsavel(self, queryset, name, value):
        """Filtra tarefas sem responsáveis atribuídos."""
        if value is None:
            return queryset
        if value:
            return queryset.filter(atribuicoes__isnull=True)
        return queryset.filter(atribuicoes__isnull=False)
    
    def filter_atrasada(self, queryset, name, value):
        """Filtra tarefas atrasadas (data_termino < hoje e status != FEITO)."""
        if value is None:
            return queryset
        hoje = timezone.now().date()
        if value:
            return queryset.filter(data_termino__lt=hoje).exclude(status='FEITO')
        return queryset.exclude(data_termino__lt=hoje, status__in=['A_FAZER', 'EM_ANDAMENTO'])
    
    def filter_minhas_tarefas(self, queryset, name, value):
        """Filtra tarefas do usuário autenticado."""
        if value is None or not hasattr(self.request, 'user'):
            return queryset
        if value:
            if self.request and hasattr(self.request, 'user'):
                return queryset.filter(atribuicoes__usuario=self.request.user)
            return queryset
        return queryset
    
    def filter_sem_sprint(self, queryset, name, value):
        """Filtra tarefas que não estão associadas a nenhuma sprint."""
        if value is None:
            return queryset
        if value:
            return queryset.filter(sprint__isnull=True)
        return queryset.filter(sprint__isnull=False)


@extend_schema_view(
    list=extend_schema(
        summary="Listar tarefas",
        description="Retorna uma lista paginada de tarefas com opções de filtragem e ordenação.",
        parameters=[
            OpenApiParameter(name="projeto", description="Filtrar por ID do projeto", type=int),
            OpenApiParameter(name="sprint", description="Filtrar por ID da sprint", type=int),
            OpenApiParameter(name="status", description="Filtrar por status (separados por vírgula)", type=str),
            OpenApiParameter(name="prioridade", description="Filtrar por prioridade (separadas por vírgula)", type=str),
            OpenApiParameter(name="responsavel", description="Filtrar por ID do usuário responsável", type=int),
            OpenApiParameter(name="atrasada", description="Filtrar tarefas atrasadas", type=bool),
            OpenApiParameter(name="minhas_tarefas", description="Filtrar minhas tarefas", type=bool),
            OpenApiParameter(name="sem_sprint", description="Filtrar tarefas sem sprint", type=bool),
            OpenApiParameter(name="ordering", description="Ordenar resultados (ex: -data_termino)", type=str),
        ],
        tags=["Tarefas"],
        responses={200: TarefaListSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Criar tarefa",
        description="Cria uma nova tarefa com os dados fornecidos.",
        tags=["Tarefas"],
        responses={201: TarefaSerializer}
    ),
    retrieve=extend_schema(
        summary="Obter detalhes da tarefa",
        description="Retorna informações detalhadas de uma tarefa específica.",
        tags=["Tarefas"],
        responses={200: TarefaSerializer}
    ),
    update=extend_schema(
        summary="Atualizar tarefa",
        description="Atualiza todos os campos de uma tarefa existente.",
        tags=["Tarefas"],
        responses={200: TarefaSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualizar tarefa parcialmente",
        description="Atualiza parcialmente os campos de uma tarefa existente.",
        tags=["Tarefas"],
        responses={200: TarefaSerializer}
    ),
    destroy=extend_schema(
        summary="Excluir tarefa",
        description="Remove permanentemente uma tarefa.",
        tags=["Tarefas"],
        responses={204: None}
    )
)
class TarefaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de tarefas.
    
    Permite criar, listar, atualizar e excluir tarefas, além de gerenciar responsáveis,
    comentários, status e associações com sprints. Inclui funcionalidades para filtrar
    tarefas por diversos critérios e obter estatísticas.
    """
    serializer_class = TarefaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TarefaFilter
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['titulo', 'data_inicio', 'data_termino', 'prioridade', 'criado_em', 'status']
    ordering = ['-criado_em']
    
    def get_serializer_class(self):
        """
        Retorna o serializer apropriado com base na ação.
        """
        if self.action == 'list':
            return TarefaListSerializer
        return TarefaSerializer
    
    def perform_create(self, serializer):
        """
        Salva a tarefa com o usuário atual como criador.
        """
        serializer.save(criado_por=self.request.user)
    
    def get_queryset(self):
        """
        Retorna o queryset otimizado com prefetch_related para atribuições e
        annotate para calcular campos derivados.
        """
        # Para a documentação da API, retornar um queryset vazio mas válido
        if getattr(self, 'swagger_fake_view', False):
            return Tarefa.objects.none()
            
        hoje = timezone.now().date()
        
        # Otimiza o queryset com prefetch_related e annotate
        queryset = Tarefa.objects.select_related('projeto', 'sprint', 'criado_por')\
            .prefetch_related(
                Prefetch('atribuicoes', queryset=AtribuicaoTarefa.objects.select_related('usuario')),
                'comentarios'
            )\
            .annotate(
                atrasada=Case(
                    When(data_termino__lt=hoje, status__in=['A_FAZER', 'EM_ANDAMENTO'], then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField()
                ),
                total_comentarios=Count('comentarios')
            )
            
        return queryset
    
    @extend_schema(
        summary="Atribuir responsável à tarefa",
        description="Atribui um usuário como responsável pela tarefa.",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'usuario_id': {
                        'type': 'integer',
                        'description': 'ID do usuário a ser atribuído como responsável'
                    }
                },
                'required': ['usuario_id']
            }
        },
        tags=["Atribuições"],
        responses={
            201: AtribuicaoTarefaSerializer,
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT
        }
    )
    @action(detail=True, methods=['post'])
    def atribuir_responsavel(self, request, pk=None):
        """Atribui um usuário como responsável pela tarefa."""
        tarefa = self.get_object()
        usuario_id = request.data.get('usuario_id')
        
        if not usuario_id:
            return Response(
                {'erro': 'É necessário fornecer um ID de usuário.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verifica se a atribuição já existe
        if AtribuicaoTarefa.objects.filter(tarefa=tarefa, usuario_id=usuario_id).exists():
            return Response(
                {'erro': 'Este usuário já está atribuído a esta tarefa.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cria a atribuição
        atribuicao = AtribuicaoTarefa.objects.create(
            tarefa=tarefa,
            usuario_id=usuario_id,
            atribuido_por=request.user
        )
        
        serializer = AtribuicaoTarefaSerializer(atribuicao)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @extend_schema(
        summary="Remover responsável da tarefa",
        description="Remove um usuário como responsável pela tarefa.",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'usuario_id': {
                        'type': 'integer',
                        'description': 'ID do usuário a ser removido da tarefa'
                    }
                },
                'required': ['usuario_id']
            }
        },
        tags=["Atribuições"],
        responses={
            204: None,
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT
        }
    )
    @action(detail=True, methods=['post'])
    def remover_responsavel(self, request, pk=None):
        """Remove um usuário como responsável pela tarefa."""
        tarefa = self.get_object()
        usuario_id = request.data.get('usuario_id')
        
        if not usuario_id:
            return Response(
                {'erro': 'É necessário fornecer um ID de usuário.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verifica se a atribuição existe
        try:
            atribuicao = AtribuicaoTarefa.objects.get(tarefa=tarefa, usuario_id=usuario_id)
            atribuicao.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AtribuicaoTarefa.DoesNotExist:
            return Response(
                {'erro': 'Este usuário não está atribuído a esta tarefa.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @extend_schema(
        summary="Adicionar comentário à tarefa",
        description="Adiciona um novo comentário à tarefa.",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'texto': {
                        'type': 'string',
                        'description': 'Texto do comentário'
                    }
                },
                'required': ['texto']
            }
        },
        tags=["Tarefas"],
        responses={
            201: ComentarioTarefaSerializer,
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT
        }
    )
    @action(detail=True, methods=['post'])
    def adicionar_comentario(self, request, pk=None):
        """Adiciona um comentário à tarefa."""
        tarefa = self.get_object()
        texto = request.data.get('texto')
        
        if not texto:
            return Response(
                {'erro': 'É necessário fornecer um texto para o comentário.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        comentario = ComentarioTarefa.objects.create(
            tarefa=tarefa,
            autor=request.user,
            texto=texto
        )
        
        serializer = ComentarioTarefaSerializer(comentario)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @extend_schema(
        summary="Associar tarefa a uma sprint",
        description="Associa a tarefa a uma sprint ou remove a associação existente.",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'sprint_id': {
                        'type': ['integer', 'null'],
                        'description': 'ID da sprint a ser associada. Use 0 ou null para remover a associação.'
                    }
                },
                'required': ['sprint_id']
            }
        },
        tags=["Tarefas"],
        responses={
            200: TarefaSerializer,
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT
        }
    )
    @action(detail=True, methods=['post'])
    def associar_sprint(self, request, pk=None):
        """Associa a tarefa a uma sprint ou remove a associação existente."""
        tarefa = self.get_object()
        sprint_id = request.data.get('sprint_id')
        
        if sprint_id is None:
            return Response(
                {'erro': 'É necessário fornecer um ID de sprint.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Se sprint_id for 0 ou vazio, remove a associação com sprint
        if not sprint_id:
            tarefa.sprint = None
            tarefa.save()
            return Response({'mensagem': 'Tarefa removida da sprint.'}, status=status.HTTP_200_OK)
        
        # Atualiza a sprint da tarefa
        tarefa.sprint_id = sprint_id
        tarefa.save()
        
        serializer = self.get_serializer(tarefa)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Atualizar status da tarefa",
        description="Atualiza o status de uma tarefa e registra a alteração no histórico.",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'status': {
                        'type': 'string',
                        'description': 'Novo status da tarefa (A_FAZER, EM_ANDAMENTO, FEITO, BLOQUEADO, CANCELADO)'
                    },
                    'comentario': {
                        'type': 'string',
                        'description': 'Comentário opcional sobre a mudança de status'
                    }
                },
                'required': ['status']
            }
        },
        tags=["Tarefas"],
        responses={
            200: TarefaSerializer,
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT
        },
        examples=[
            OpenApiExample(
                'Exemplo de atualização para Em Andamento',
                value={'status': 'EM_ANDAMENTO', 'comentario': 'Iniciando o desenvolvimento'},
                status_codes=[200]
            ),
            OpenApiExample(
                'Exemplo de atualização para Concluído',
                value={'status': 'FEITO', 'comentario': 'Tarefa finalizada conforme requisitos'},
                status_codes=[200]
            )
        ]
    )
    @action(detail=True, methods=['post'])
    def atualizar_status(self, request, pk=None):
        """Atualiza o status de uma tarefa e registra a alteração no histórico."""
        tarefa = self.get_object()
        novo_status = request.data.get('status')
        comentario = request.data.get('comentario', '')
        
        if not novo_status:
            return Response(
                {'erro': 'É necessário fornecer um status.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verifica se o status é válido
        if novo_status not in dict(Tarefa.STATUS_CHOICES).keys():
            return Response(
                {'erro': f'Status inválido. Opções válidas: {dict(Tarefa.STATUS_CHOICES).keys()}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Se o status for o mesmo, retorna erro
        if tarefa.status == novo_status:
            return Response(
                {'erro': 'A tarefa já está com este status.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Atualiza o status
        status_anterior = tarefa.status
        tarefa.status = novo_status
        tarefa.save()
        
        # Registra a alteração no histórico
        HistoricoStatusTarefa.objects.create(
            tarefa=tarefa,
            status_anterior=status_anterior,
            novo_status=novo_status,
            alterado_por=request.user,
            comentario=comentario
        )
        
        # Retorna a tarefa atualizada
        serializer = self.get_serializer(tarefa)
        return Response(serializer.data)
        
    @extend_schema(
        summary="Obter histórico de status da tarefa",
        description="Retorna o histórico de alterações de status da tarefa.",
        tags=["Tarefas"],
        responses={200: HistoricoStatusTarefaSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def historico_status(self, request, pk=None):
        """Retorna o histórico de alterações de status da tarefa."""
        tarefa = self.get_object()
        historico = HistoricoStatusTarefa.objects.filter(tarefa=tarefa)\
            .select_related('alterado_por')\
            .order_by('-alterado_em')
        
        serializer = HistoricoStatusTarefaSerializer(historico, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="Listar atribuições de tarefas",
        description="Retorna uma lista de atribuições de tarefas a usuários.",
        parameters=[
            OpenApiParameter(name="tarefa", description="Filtrar por ID da tarefa", type=int),
            OpenApiParameter(name="usuario", description="Filtrar por ID do usuário", type=int),
        ],
        tags=["Atribuições"],
        responses={200: AtribuicaoTarefaSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Criar atribuição de tarefa",
        description="Atribui uma tarefa a um usuário.",
        tags=["Atribuições"],
        responses={201: AtribuicaoTarefaSerializer}
    ),
    retrieve=extend_schema(
        summary="Obter detalhes de atribuição",
        description="Retorna informações detalhadas de uma atribuição específica.",
        tags=["Atribuições"],
        responses={200: AtribuicaoTarefaSerializer}
    ),
    destroy=extend_schema(
        summary="Remover atribuição",
        description="Remove a atribuição de uma tarefa a um usuário.",
        tags=["Atribuições"],
        responses={204: None}
    )
)
class AtribuicaoTarefaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de atribuições de tarefas a usuários.
    
    Permite criar, listar, visualizar e remover atribuições de tarefas a usuários.
    O usuário que faz a atribuição é automaticamente registrado.
    """
    serializer_class = AtribuicaoTarefaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['tarefa', 'usuario']
    ordering_fields = ['atribuido_em']
    ordering = ['-atribuido_em']
    
    def get_queryset(self):
        """
        Retorna o queryset otimizado com select_related para tarefa e usuário.
        """
        return AtribuicaoTarefa.objects.select_related('tarefa', 'usuario', 'atribuido_por')
    
    def perform_create(self, serializer):
        """
        Salva a atribuição com o usuário atual como atribuidor.
        """
        serializer.save(atribuido_por=self.request.user)


@extend_schema_view(
    list=extend_schema(
        summary="Listar comentários de tarefas",
        description="Retorna uma lista de comentários de tarefas.",
        parameters=[
            OpenApiParameter(name="tarefa", description="Filtrar por ID da tarefa", type=int),
            OpenApiParameter(name="autor", description="Filtrar por ID do autor", type=int),
            OpenApiParameter(name="ordering", description="Ordenar resultados (ex: -criado_em)", type=str),
        ],
        tags=["Comentários de Tarefas"],
        responses={200: ComentarioTarefaSerializer(many=True)}
    ),
    create=extend_schema(
        summary="Criar comentário",
        description="Adiciona um novo comentário a uma tarefa.",
        tags=["Comentários de Tarefas"],
        responses={201: ComentarioTarefaSerializer}
    ),
    retrieve=extend_schema(
        summary="Obter detalhes de comentário",
        description="Retorna informações detalhadas de um comentário específico.",
        tags=["Comentários de Tarefas"],
        responses={200: ComentarioTarefaSerializer}
    ),
    update=extend_schema(
        summary="Atualizar comentário",
        description="Atualiza o texto de um comentário existente.",
        tags=["Comentários de Tarefas"],
        responses={200: ComentarioTarefaSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualizar comentário parcialmente",
        description="Atualiza parcialmente o texto de um comentário existente.",
        tags=["Comentários de Tarefas"],
        responses={200: ComentarioTarefaSerializer}
    ),
    destroy=extend_schema(
        summary="Excluir comentário",
        description="Remove permanentemente um comentário.",
        tags=["Comentários de Tarefas"],
        responses={204: None}
    )
)
class ComentarioTarefaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de comentários de tarefas.
    
    Permite criar, listar, visualizar, atualizar e remover comentários de tarefas.
    O usuário autenticado é automaticamente definido como autor do comentário.
    """
    serializer_class = ComentarioTarefaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tarefa', 'autor']
    search_fields = ['texto']
    ordering_fields = ['criado_em']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        """
        Retorna o queryset otimizado com select_related para tarefa e autor.
        """
        return ComentarioTarefa.objects.select_related('tarefa', 'autor')
    
    def perform_create(self, serializer):
        """
        Salva o comentário com o usuário atual como autor.
        """
        serializer.save(autor=self.request.user)
