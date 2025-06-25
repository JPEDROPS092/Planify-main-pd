"""
Django filters for the projects app.
Provides advanced filtering capabilities for API endpoints.
"""
import django_filters
from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import FilterSet, DateFromToRangeFilter, CharFilter, BooleanFilter
from .models import Projeto, Sprint, MembroProjeto, HistoricoStatusProjeto


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
    
    # Advanced text search across multiple fields
    search = django_filters.CharFilter(method='filter_search', label='Search')
    
    # Advanced date range filters
    created_after = django_filters.DateFilter(field_name='criado_em', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='criado_em', lookup_expr='lte')
    
    # Boolean filters
    has_sprints = django_filters.BooleanFilter(method='filter_has_sprints')
    
    # Related field filters
    criado_por = django_filters.ModelChoiceFilter(
        queryset=None,  # Will be set in __init__
        field_name='criado_por'
    )
    
    # Member filter by username
    member = django_filters.CharFilter(method='filter_member', label='Member Username')
    
    class Meta:
        model = Projeto
        # Include only actual model fields, not custom filters
        fields = [
            'titulo', 'descricao', 'status', 'prioridade', 'arquivado',
            'data_inicio', 'data_fim', 'criado_por'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set queryset for user filter
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.filters['criado_por'].queryset = User.objects.all()
    
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
    
    def filter_search(self, queryset, name, value):
        """
        Search across title and description.
        """
        if value:
            return queryset.filter(
                Q(titulo__icontains=value) | 
                Q(descricao__icontains=value)
            )
        return queryset
    
    def filter_has_sprints(self, queryset, name, value):
        """
        Filter projects that have sprints.
        """
        if value is True:
            return queryset.filter(sprints__isnull=False).distinct()
        elif value is False:
            return queryset.filter(sprints__isnull=True)
        return queryset
    
    def filter_member(self, queryset, name, value):
        """
        Filter projects by member username.
        """
        if value:
            return queryset.filter(
                membros__usuario__username__icontains=value
            ).distinct()
        return queryset


class SprintFilter(FilterSet):
    """
    Filter set for Sprint model.
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
    
    # Text search
    search = django_filters.CharFilter(method='filter_search', label='Search')
    
    class Meta:
        model = Sprint
        # Include only actual model fields, not custom filters
        fields = ['nome', 'status', 'projeto', 'data_inicio', 'data_fim']
    
    def filter_ativa(self, queryset, name, value):
        """Filtra sprints que estão ativas no momento."""
        hoje = timezone.now().date()
        if value:
            return queryset.filter(data_inicio__lte=hoje, data_fim__gte=hoje)
        return queryset
    
    def filter_search(self, queryset, name, value):
        """
        Search across sprint name and description.
        """
        if value:
            return queryset.filter(
                Q(nome__icontains=value) | 
                Q(descricao__icontains=value)
            )
        return queryset


class HistoricoStatusProjetoFilter(FilterSet):
    """
    Filter set for project status history.
    """
    projeto = CharFilter(field_name='projeto__id', help_text="Filtra por ID do projeto")
    projeto_titulo = CharFilter(field_name='projeto__titulo', lookup_expr='icontains', 
                           help_text="Filtra por título do projeto (case insensitive)")
    alterado_por = CharFilter(field_name='alterado_por__id', help_text="Filtra por ID do usuário que alterou")
    alterado_por_username = CharFilter(field_name='alterado_por__username', lookup_expr='icontains', 
                                  help_text="Filtra por username do usuário que alterou (case insensitive)")
    alterado_em_apos = DateFromToRangeFilter(field_name='alterado_em', lookup_expr='gte', 
                                         help_text="Filtra registros alterados após a data especificada")
    alterado_em_antes = DateFromToRangeFilter(field_name='alterado_em', lookup_expr='lte', 
                                          help_text="Filtra registros alterados antes da data especificada")
    status_anterior = CharFilter(method='filter_status_anterior', 
                             help_text="Filtra por status anterior (pode ser múltiplos, separados por vírgula)")
    
    class Meta:
        model = HistoricoStatusProjeto
        # Include only actual model fields, not custom filters
        fields = ['projeto', 'status_anterior', 'alterado_por', 'alterado_em']
    
    def filter_status_anterior(self, queryset, name, value):
        """Filtra por múltiplos status anteriores separados por vírgula."""
        if not value:
            return queryset
        status_list = [s.strip().upper() for s in value.split(',')]
        return queryset.filter(status_anterior__in=status_list)


class MembroProjetoFilter(django_filters.FilterSet):
    """
    Filter set for Project Members.
    """
    
    # Role filter
    papel = django_filters.MultipleChoiceFilter(
        choices=MembroProjeto.PAPEL_CHOICES,
        lookup_expr='in'
    )
    
    # User search
    user_search = django_filters.CharFilter(method='filter_user_search')
    
    # Project filter
    projeto = django_filters.ModelChoiceFilter(
        queryset=Projeto.objects.all(),
        field_name='projeto'
    )
    
    class Meta:
        model = MembroProjeto
        fields = ['papel', 'projeto']
    
    def filter_user_search(self, queryset, name, value):
        """
        Search members by username, email, or name.
        """
        if value:
            return queryset.filter(
                Q(usuario__username__icontains=value) |
                Q(usuario__email__icontains=value) |
                Q(usuario__first_name__icontains=value) |
                Q(usuario__last_name__icontains=value)
            )
        return queryset
