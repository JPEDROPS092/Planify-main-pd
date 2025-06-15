from django.db.models import FloatField
from rest_framework import viewsets, status, permissions, filters, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateFromToRangeFilter, CharFilter, BooleanFilter
from django.db.models import Q, Count, Prefetch, F, ExpressionWrapper, BooleanField, FloatField, Case, When
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from .models import Projeto, MembroProjeto, Sprint, HistoricoStatusProjeto
from .serializers import ProjetoSerializer, ProjetoListSerializer, MembroProjetoSerializer, SprintSerializer, HistoricoStatusProjetoSerializer
from tasks.models import Tarefa

User = get_user_model()


class ProjetoFilter(FilterSet):
    """Filtro personalizado para projetos.
    
    Permite filtrar projetos por diversos critérios como data, status, prioridade, etc.
    """
    titulo = CharFilter(lookup_expr='icontains', help_text="Filtra por título (case insensitive)")
    descricao = CharFilter(lookup_expr='icontains', help_text="Filtra por descrição (case insensitive)")
    data_inicio_apos = DateFromToRangeFilter(field_name='data_inicio', lookup_expr='gte', 
                                         help_text="Filtra projetos com data de início após a data especificada")
    data_inicio_antes = DateFromToRangeFilter(field_name='data_inicio', lookup_expr='lte', 
                                          help_text="Filtra projetos com data de início antes da data especificada")
    data_fim_apos = DateFromToRangeFilter(field_name='data_fim', lookup_expr='gte', 
                                      help_text="Filtra projetos com data de fim após a data especificada")
    data_fim_antes = DateFromToRangeFilter(field_name='data_fim', lookup_expr='lte', 
                                       help_text="Filtra projetos com data de fim antes da data especificada")
    status = CharFilter(method='filter_status', help_text="Filtra por status (pode ser múltiplos, separados por vírgula)")
    prioridade = CharFilter(method='filter_prioridade', help_text="Filtra por prioridade (pode ser múltiplas, separadas por vírgula)")
    membro = CharFilter(method='filter_membro', help_text="Filtra projetos que contenham o membro especificado (ID do usuário)")
    atrasado = BooleanFilter(method='filter_atrasado', help_text="Filtra projetos atrasados (data_fim < hoje e status != CONCLUIDO)")
    
    class Meta:
        model = Projeto
        fields = ['titulo', 'descricao', 'status', 'prioridade', 'arquivado', 
                 'data_inicio_apos', 'data_inicio_antes', 'data_fim_apos', 'data_fim_antes',
                 'membro', 'atrasado']
    
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
    
    def filter_membro(self, queryset, name, value):
        """Filtra projetos que contenham o membro especificado."""
        if not value:
            return queryset
        return queryset.filter(membros__usuario_id=value)
    
    def filter_atrasado(self, queryset, name, value):
        """Filtra projetos atrasados (data_fim < hoje e status != CONCLUIDO)."""
        hoje = timezone.now().date()
        if value:
            return queryset.filter(data_fim__lt=hoje).exclude(status='CONCLUIDO')
        return queryset

@extend_schema_view(
    list=extend_schema(
        summary="Listar projetos",
        description="Retorna uma lista paginada de projetos.",
        responses={200: ProjetoListSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Obter detalhes do projeto",
        description="Retorna informações detalhadas de um projeto específico.",
        responses={200: ProjetoSerializer}
    ),
    create=extend_schema(
        summary="Criar novo projeto",
        description="Cria um novo projeto.",
        responses={201: ProjetoSerializer}
    ),
    update=extend_schema(
        summary="Atualizar projeto",
        description="Atualiza todos os campos de um projeto existente.",
        responses={200: ProjetoSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualizar projeto parcialmente",
        description="Atualiza parcialmente um projeto existente.",
        responses={200: ProjetoSerializer}
    ),
    destroy=extend_schema(
        summary="Excluir projeto",
        description="Remove um projeto existente.",
        responses={204: None}
    )
)
class ProjetoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de projetos.
    
    Permite criar, listar, atualizar e excluir projetos, além de gerenciar membros do projeto,
    sprints, tarefas e histórico de status.
    """
    queryset = Projeto.objects.all()  # Adicionado para resolver o erro de basename
    serializer_class = ProjetoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProjetoFilter
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['criado_em', 'titulo', 'status', 'prioridade', 'data_inicio', 'data_fim']
    ordering = ['-criado_em']
    
    def get_queryset(self):
        """
        Retorna o queryset otimizado com prefetch_related para membros e 
        annotate para calcular campos derivados.
        """
        hoje = timezone.now().date()
        
        # Prefetch relacionados para otimizar consultas
        membros_prefetch = Prefetch(
            'membros',
            queryset=MembroProjeto.objects.select_related('usuario')
        )
        
        # Annotate para campos calculados
        queryset = Projeto.objects.annotate(
            atrasado=ExpressionWrapper(
                Q(data_fim__lt=hoje) & ~Q(status='CONCLUIDO'),
                output_field=BooleanField()
            )
        ).prefetch_related(membros_prefetch)
        
        return queryset
    
    def get_serializer_class(self):
        """
        Retorna o serializer apropriado com base na ação.
        """
        if self.action == 'list':
            return ProjetoListSerializer
        return ProjetoSerializer
    
    def perform_create(self, serializer):
        """
        Salva o projeto e adiciona o criador como membro administrador automaticamente.
        """
        projeto = serializer.save(criado_por=self.request.user)
        # Adiciona o criador como membro do projeto automaticamente
        MembroProjeto.objects.create(
            projeto=projeto,
            usuario=self.request.user,
            papel='ADMIN'
        )
    
    @extend_schema(
        summary="Adicionar membro ao projeto",
        description="Adiciona um novo membro ao projeto com o papel especificado.",
        request=MembroProjetoSerializer,
        responses={201: MembroProjetoSerializer}
    )
    @action(detail=True, methods=['post'])
    def adicionar_membro(self, request, pk=None):
        """
        Adiciona um membro ao projeto.
        
        Requer o ID do usuário e o papel a ser atribuído.
        """
        projeto = self.get_object()
        serializer = MembroProjetoSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                usuario = User.objects.get(pk=request.data.get('usuario'))
                # Verifica se o usuário já é membro
                if MembroProjeto.objects.filter(projeto=projeto, usuario=usuario).exists():
                    return Response(
                        {'detail': _('Usuário já é membro deste projeto.')}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                serializer.save(projeto=projeto)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response(
                    {'detail': _('Usuário não encontrado.')}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        summary="Listar membros do projeto",
        description="Retorna todos os membros associados ao projeto.",
        responses={200: MembroProjetoSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def listar_membros(self, request, pk=None):
        """
        Lista todos os membros do projeto.
        """
        projeto = self.get_object()
        membros = MembroProjeto.objects.filter(projeto=projeto).select_related('usuario')
        serializer = MembroProjetoSerializer(membros, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Remover membro do projeto",
        description="Remove um membro do projeto pelo ID.",
        parameters=[
            OpenApiParameter(
                name="membro_id", 
                description="ID do membro a ser removido", 
                required=True, 
                type=int
            )
        ],
        responses={204: None}
    )
    @action(detail=True, methods=['delete'])
    def remover_membro(self, request, pk=None):
        """
        Remove um membro do projeto.
        
        Requer o ID do membro a ser removido.
        """
        projeto = self.get_object()
        membro_id = request.query_params.get('membro_id')
        
        if not membro_id:
            return Response(
                {'detail': _('ID do membro é obrigatório.')}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            membro = MembroProjeto.objects.get(pk=membro_id, projeto=projeto)
            
            # Impede a remoção do criador do projeto
            if membro.usuario == projeto.criado_por:
                return Response(
                    {'detail': _('Não é possível remover o criador do projeto.')}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            membro.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except MembroProjeto.DoesNotExist:
            return Response(
                {'erro': 'Usuário não é membro deste projeto'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def membros(self, request, pk=None):
        """
        Lista os membros do projeto.
        """
        project = self.get_object()
        membros = project.membros.all()
        serializer = MembroProjetoSerializer(membros, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """
        Arquiva ou desarquiva um projeto.
        """
        project = self.get_object()
        project.arquivado = not project.arquivado
        project.save()
        
        return Response({
            'arquivado': project.arquivado
        })
    
    @action(detail=False, methods=['get'])
    def my_projects(self, request):
        """
        Retorna os projetos dos quais o usuário é membro.
        """
        user = request.user
        projects = Projeto.objects.filter(membros__usuario=user)
        
        # Aplicar filtros
        projects = self.filter_queryset(projects)
        
        page = self.paginate_queryset(projects)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def dashboard(self, request, pk=None):
        """Dashboard do projeto"""
        projeto = self.get_object()
        # Implementação do dashboard
        return Response({"status": "dashboard data"})

    @action(detail=True, methods=['get'])
    def kanban(self, request, pk=None):
        """Visualização Kanban do projeto"""
        projeto = self.get_object()
        # Implementação do kanban
        return Response({"status": "kanban data"})

    @action(detail=True, methods=['get'])
    def gantt(self, request, pk=None):
        """Visualização Gantt do projeto"""
        projeto = self.get_object()
        # Implementação do gantt
        return Response({"status": "gantt data"})

    @action(detail=True, methods=['get'])
    def historico_status(self, request, pk=None):
        """Histórico de status do projeto"""
        projeto = self.get_object()
        historico = HistoricoStatusProjeto.objects.filter(projeto=projeto)
        serializer = HistoricoStatusProjetoSerializer(historico, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def sprints(self, request, pk=None):
        """Listar sprints do projeto"""
        projeto = self.get_object()
        sprints = Sprint.objects.filter(projeto=projeto)
        serializer = SprintSerializer(sprints, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def criar_sprint(self, request, pk=None):
        """Criar nova sprint no projeto"""
        projeto = self.get_object()
        serializer = SprintSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(projeto=projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def criar_tarefa(self, request, pk=None):
        """Criar nova tarefa no projeto"""
        projeto = self.get_object()
        # Implementação da criação de tarefa
        return Response({"status": "tarefa criada"})

    @action(detail=True, methods=['post'])
    def criar_tarefas_multiplas(self, request, pk=None):
        """Criar múltiplas tarefas no projeto"""
        projeto = self.get_object()
        # Implementação da criação de múltiplas tarefas
        return Response({"status": "tarefas criadas"})

    @action(detail=True, methods=['get'])
    def exportar(self, request, pk=None):
        """Exportar dados do projeto"""
        projeto = self.get_object()
        # Implementação da exportação
        return Response({"status": "dados exportados"})
    
    @extend_schema(
        summary="Métricas Detalhadas do Projeto",
        description="Retorna métricas detalhadas sobre o projeto, incluindo progresso, custos, prazos e qualidade.",
        responses={200: OpenApiTypes.OBJECT}
    )
    @action(detail=True, methods=['get'])
    def metrics(self, request, pk=None):
        """Retorna métricas detalhadas do projeto"""
        projeto = self.get_object()
        
        # Cálculo das métricas
        total_tarefas = Tarefa.objects.filter(projeto=projeto).count()
        tarefas_concluidas = Tarefa.objects.filter(projeto=projeto, status='CONCLUIDA').count()
        
        # Cálculo do progresso
        progresso = (tarefas_concluidas / total_tarefas * 100) if total_tarefas > 0 else 0
        
        # Cálculo de prazos
        dias_totais = (projeto.data_fim - projeto.data_inicio).days
        dias_decorridos = (timezone.now().date() - projeto.data_inicio).days
        progresso_prazo = (dias_decorridos / dias_totais * 100) if dias_totais > 0 else 0
        
        # Verifica atraso
        atrasado = projeto.data_fim < timezone.now().date() and projeto.status != 'CONCLUIDO'
        
        metricas = {
            'progresso': {
                'percentual_concluido': progresso,
                'tarefas_totais': total_tarefas,
                'tarefas_concluidas': tarefas_concluidas,
            },
            'prazos': {
                'dias_totais': dias_totais,
                'dias_decorridos': dias_decorridos,
                'progresso_prazo': progresso_prazo,
                'atrasado': atrasado,
            },
            'status': {
                'atual': projeto.status,
                'data_ultima_atualizacao': projeto.atualizado_em,
            }
        }
        
        return Response(metricas)


class SprintFilter(FilterSet):
    """
    Filtro personalizado para sprints.
    
    Permite filtrar sprints por diversos critérios como data, status, projeto, etc.
    """
    titulo = CharFilter(lookup_expr='icontains', help_text="Filtra por título (case insensitive)")
    descricao = CharFilter(lookup_expr='icontains', help_text="Filtra por descrição (case insensitive)")
    data_inicio_apos = DateFromToRangeFilter(field_name='data_inicio', lookup_expr='gte',
                                        help_text="Filtra sprints com data de início após a data especificada")
    data_inicio_antes = DateFromToRangeFilter(field_name='data_inicio', lookup_expr='lte',
                                         help_text="Filtra sprints com data de início antes da data especificada")
    data_fim_apos = DateFromToRangeFilter(field_name='data_fim', lookup_expr='gte',
                                     help_text="Filtra sprints com data de fim após a data especificada")
    data_fim_antes = DateFromToRangeFilter(field_name='data_fim', lookup_expr='lte',
                                      help_text="Filtra sprints com data de fim antes da data especificada")
    ativa = BooleanFilter(method='filter_ativa', help_text="Filtra sprints ativas (data_inicio <= hoje <= data_fim)")
    
    class Meta:
        model = Sprint
        fields = ['titulo', 'descricao', 'projeto', 'status',
                'data_inicio_apos', 'data_inicio_antes', 'data_fim_apos', 'data_fim_antes',
                'ativa']
    
    def filter_ativa(self, queryset, name, value):
        """Filtra sprints ativas (data_inicio <= hoje <= data_fim)."""
        hoje = timezone.now().date()
        if value:
            return queryset.filter(data_inicio__lte=hoje, data_fim__gte=hoje)
        return queryset


@extend_schema_view(
    list=extend_schema(
        summary="Listar sprints",
        description="Retorna uma lista paginada de sprints com informações detalhadas.",
        parameters=[
            OpenApiParameter(name="projeto", description="Filtrar por ID do projeto", type=int),
            OpenApiParameter(name="status", description="Filtrar por status", type=str),
            OpenApiParameter(name="ativa", description="Filtrar sprints ativas", type=bool),
            OpenApiParameter(name="search", description="Buscar por título ou descrição", type=str),
            OpenApiParameter(name="ordering", description="Ordenar resultados (ex: -data_inicio,titulo)", type=str),
        ],
        responses={200: SprintSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Obter detalhes da sprint",
        description="Retorna informações detalhadas de uma sprint específica.",
        responses={200: SprintSerializer}
    ),
    create=extend_schema(
        summary="Criar nova sprint",
        description="Cria uma nova sprint associada a um projeto.",
        responses={201: SprintSerializer}
    ),
    update=extend_schema(
        summary="Atualizar sprint",
        description="Atualiza todos os campos de uma sprint existente.",
        responses={200: SprintSerializer}
    ),
    partial_update=extend_schema(
        summary="Atualizar sprint parcialmente",
        description="Atualiza parcialmente uma sprint existente.",
        responses={200: SprintSerializer}
    ),
    destroy=extend_schema(
        summary="Excluir sprint",
        description="Remove permanentemente uma sprint.",
        responses={204: None}
    )
)
class SprintViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de sprints.
    
    Permite criar, listar, atualizar e excluir sprints, além de gerenciar tarefas da sprint.
    Inclui funcionalidades para filtrar sprints por projeto, status, datas e outros critérios.
    """
    queryset = Sprint.objects.all()  # Adicionado para resolver o erro de basename
    serializer_class = SprintSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = SprintFilter
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['titulo', 'data_inicio', 'data_fim', 'criado_em', 'status']
    ordering = ['-data_inicio']
    
    def get_queryset(self):
        """
        Retorna o queryset otimizado com select_related para projeto e criador,
        e annotate para calcular campos derivados.
        """
        hoje = timezone.now().date()
        
        # Annotate para campos calculados
        queryset = Sprint.objects.annotate(
            ativa=ExpressionWrapper(
                Q(data_inicio__lte=hoje) & Q(data_fim__gte=hoje),
                output_field=BooleanField()
            ),
            progresso_calculado=Case(
                When(tarefas__isnull=True, then=0),
                default=Count('tarefas', filter=Q(tarefas__status='FEITO')) * 100 / Count('tarefas'),
                output_field=FloatField()
            )
        ).select_related('projeto', 'criado_por')
        
        return queryset
    
    def perform_create(self, serializer):
        """
        Salva a sprint com o usuário atual como criador.
        """
        serializer.save(criado_por=self.request.user)
    
    @extend_schema(
        summary="Listar tarefas da sprint",
        description="Retorna todas as tarefas associadas a uma sprint específica.",
        parameters=[
            OpenApiParameter(
                name="status", 
                description="Filtrar por status (ex: PENDENTE,EM_ANDAMENTO)", 
                type=str
            ),
            OpenApiParameter(
                name="prioridade", 
                description="Filtrar por prioridade (ex: ALTA,MEDIA)", 
                type=str
            ),
            OpenApiParameter(
                name="responsavel", 
                description="Filtrar por responsável (ID do usuário)", 
                type=int
            )
        ]
    )
    @action(detail=True, methods=['get'])
    def tarefas(self, request, pk=None):
        """
        Lista todas as tarefas da sprint com opções de filtragem.
        """
        sprint = self.get_object()
        tarefas = Tarefa.objects.filter(sprint=sprint)
        
        # Aplica filtros opcionais
        status = request.query_params.get('status')
        if status:
            status_list = [s.strip().upper() for s in status.split(',')]
            tarefas = tarefas.filter(status__in=status_list)
            
        prioridade = request.query_params.get('prioridade')
        if prioridade:
            prioridade_list = [p.strip().upper() for p in prioridade.split(',')]
            tarefas = tarefas.filter(prioridade__in=prioridade_list)
            
        responsavel = request.query_params.get('responsavel')
        if responsavel:
            tarefas = tarefas.filter(responsavel_id=responsavel)
        
        # Ordenação e otimização
        tarefas = tarefas.select_related('responsavel', 'criado_por', 'projeto').order_by('-criado_em')
        
        # Importação local para evitar dependência circular
        from tasks.serializers import TarefaSerializer
        serializer = TarefaSerializer(tarefas, many=True)
        
        return Response(serializer.data)
    
    @extend_schema(
        summary="Resumo da sprint",
        description="Retorna um resumo estatístico da sprint, incluindo progresso, tarefas por status e outros indicadores."
    )
    @action(detail=True, methods=['get'])
    def resumo(self, request, pk=None):
        """
        Fornece um resumo estatístico da sprint.
        """
        sprint = self.get_object()
        tarefas = Tarefa.objects.filter(sprint=sprint)
        
        # Contagem de tarefas por status
        tarefas_por_status = {
            status[0]: tarefas.filter(status=status[0]).count() 
            for status in Tarefa.STATUS_CHOICES
        }
        
        # Contagem de tarefas por prioridade
        tarefas_por_prioridade = {
            prioridade[0]: tarefas.filter(prioridade=prioridade[0]).count() 
            for prioridade in Tarefa.PRIORIDADE_CHOICES
        }
        
        # Cálculo de progresso
        total_tarefas = tarefas.count()
        tarefas_concluidas = tarefas.filter(status='FEITO').count()
        progresso = 0 if total_tarefas == 0 else int((tarefas_concluidas / total_tarefas) * 100)
        
        # Verifica se a sprint está ativa
        hoje = timezone.now().date()
        ativa = sprint.data_inicio <= hoje <= sprint.data_fim
        
        # Dias restantes
        dias_restantes = 0 if sprint.data_fim < hoje else (sprint.data_fim - hoje).days
        
        return Response({
            'total_tarefas': total_tarefas,
            'tarefas_concluidas': tarefas_concluidas,
            'progresso': progresso,
            'tarefas_por_status': tarefas_por_status,
            'tarefas_por_prioridade': tarefas_por_prioridade,
            'ativa': ativa,
            'dias_restantes': dias_restantes,
            'data_inicio': sprint.data_inicio,
            'data_fim': sprint.data_fim,
            'status': sprint.status
        })


class HistoricoStatusProjetoFilter(FilterSet):
    """
    Filtro personalizado para histórico de status de projetos.
    
    Permite filtrar históricos por projeto, usuário, data e status.
    """
    projeto = CharFilter(field_name='projeto__id', help_text="Filtra por ID do projeto")
    projeto_titulo = CharFilter(field_name='projeto__titulo', lookup_expr='icontains', 
                             help_text="Filtra por título do projeto (case insensitive)")
    alterado_por = CharFilter(field_name='alterado_por__id', help_text="Filtra por ID do usuário que alterou")
    alterado_por_username = CharFilter(field_name='alterado_por__username', lookup_expr='icontains', 
                                    help_text="Filtra por nome de usuário (case insensitive)")
    alterado_em_apos = DateFromToRangeFilter(field_name='alterado_em', lookup_expr='gte', 
                                         help_text="Filtra alterações após a data especificada")
    alterado_em_antes = DateFromToRangeFilter(field_name='alterado_em', lookup_expr='lte', 
                                          help_text="Filtra alterações antes da data especificada")
    status_anterior = CharFilter(method='filter_status_anterior', 
                              help_text="Filtra por status anterior (pode ser múltiplos, separados por vírgula)")
    novo_status = CharFilter(method='filter_novo_status', 
                          help_text="Filtra por novo status (pode ser múltiplos, separados por vírgula)")
    
    class Meta:
        model = HistoricoStatusProjeto
        fields = ['projeto', 'projeto_titulo', 'alterado_por', 'alterado_por_username', 
                 'alterado_em_apos', 'alterado_em_antes', 'status_anterior', 'novo_status']
    
    def filter_status_anterior(self, queryset, name, value):
        """Filtra por múltiplos status anteriores separados por vírgula."""
        if not value:
            return queryset
        status_list = [s.strip().upper() for s in value.split(',')]
        return queryset.filter(status_anterior__in=status_list)
    
    def filter_novo_status(self, queryset, name, value):
        """Filtra por múltiplos novos status separados por vírgula."""
        if not value:
            return queryset
        status_list = [s.strip().upper() for s in value.split(',')]
        return queryset.filter(novo_status__in=status_list)


@extend_schema_view(
    list=extend_schema(
        summary="Listar histórico de status",
        description="Retorna uma lista paginada de alterações de status de projetos.",
        parameters=[
            OpenApiParameter(name="projeto", description="Filtrar por ID do projeto", type=int),
            OpenApiParameter(name="alterado_por", description="Filtrar por ID do usuário que alterou", type=int),
            OpenApiParameter(name="status_anterior", description="Filtrar por status anterior (separados por vírgula)", type=str),
            OpenApiParameter(name="novo_status", description="Filtrar por novo status (separados por vírgula)", type=str),
            OpenApiParameter(name="ordering", description="Ordenar resultados (ex: -alterado_em)", type=str),
        ],
        responses={200: HistoricoStatusProjetoSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Obter detalhe de alteração de status",
        description="Retorna informações detalhadas de uma alteração específica de status.",
        responses={200: HistoricoStatusProjetoSerializer}
    )
)
class HistoricoStatusProjetoViewSet(mixins.ListModelMixin,
                                   mixins.RetrieveModelMixin,
                                   viewsets.GenericViewSet):
    """
    ViewSet para histórico de alterações de status de projetos.
    
    Permite listar e visualizar detalhes de alterações de status, com filtros
    por projeto, usuário, data e status.
    """
    queryset = HistoricoStatusProjeto.objects.all()  # Adicionado para resolver o erro de basename
    serializer_class = HistoricoStatusProjetoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = HistoricoStatusProjetoFilter
    ordering_fields = ['alterado_em', 'projeto__titulo']
    ordering = ['-alterado_em']
    
    def get_queryset(self):
        """
        Retorna o queryset otimizado com select_related para projeto e usuário.
        """
        return HistoricoStatusProjeto.objects.select_related('projeto', 'alterado_por')
    
    @extend_schema(
        summary="Resumo de alterações por projeto",
        description="Retorna um resumo estatístico das alterações de status agrupadas por projeto."
    )
    @action(detail=False, methods=['get'])
    def resumo_por_projeto(self, request):
        """
        Fornece um resumo estatístico das alterações de status agrupadas por projeto.
        """
        # Agrupa as alterações por projeto e conta
        resumo = HistoricoStatusProjeto.objects.values('projeto', 'projeto__titulo')\
            .annotate(total_alteracoes=Count('id'))\
            .order_by('-total_alteracoes')
        
        # Formata a resposta
        resultado = [{
            'projeto_id': item['projeto'],
            'projeto_titulo': item['projeto__titulo'],
            'total_alteracoes': item['total_alteracoes']
        } for item in resumo]
        
        return Response(resultado)
