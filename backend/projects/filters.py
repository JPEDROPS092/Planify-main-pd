"""
Django filters for the projects app.
Provides advanced filtering capabilities for API endpoints.
"""
import django_filters
from django.db.models import Q
from .models import Projeto, Sprint, MembroProjeto


class ProjetoFilter(django_filters.FilterSet):
    """
    Filter set for Project model with advanced filtering options.
    """
    
    # Text search across multiple fields
    search = django_filters.CharFilter(method='filter_search', label='Search')
    
    # Date range filters
    created_after = django_filters.DateFilter(field_name='criado_em', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='criado_em', lookup_expr='lte')
    start_after = django_filters.DateFilter(field_name='data_inicio', lookup_expr='gte')
    start_before = django_filters.DateFilter(field_name='data_inicio', lookup_expr='lte')
    
    # Multi-choice filters
    status = django_filters.MultipleChoiceFilter(
        choices=Projeto.STATUS_CHOICES,
        lookup_expr='in'
    )
    prioridade = django_filters.MultipleChoiceFilter(
        choices=Projeto.PRIORIDADE_CHOICES,
        lookup_expr='in'
    )
    
    # Boolean filters
    arquivado = django_filters.BooleanFilter()
    has_sprints = django_filters.BooleanFilter(method='filter_has_sprints')
    
    # Related field filters
    criado_por = django_filters.ModelChoiceFilter(
        queryset=None,  # Will be set in __init__
        field_name='criado_por'
    )
    
    # Member filter
    member = django_filters.CharFilter(method='filter_member', label='Member Username')
    
    class Meta:
        model = Projeto
        fields = [
            'status', 'prioridade', 'arquivado', 'criado_por',
            'search', 'created_after', 'created_before',
            'start_after', 'start_before', 'has_sprints', 'member'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set queryset for user filter
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.filters['criado_por'].queryset = User.objects.all()
    
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


class SprintFilter(django_filters.FilterSet):
    """
    Filter set for Sprint model.
    """
    
    # Text search
    search = django_filters.CharFilter(method='filter_search', label='Search')
    
    # Date filters
    start_after = django_filters.DateFilter(field_name='data_inicio', lookup_expr='gte')
    start_before = django_filters.DateFilter(field_name='data_inicio', lookup_expr='lte')
    end_after = django_filters.DateFilter(field_name='data_fim', lookup_expr='gte')
    end_before = django_filters.DateFilter(field_name='data_fim', lookup_expr='lte')
    
    # Status filter
    status = django_filters.MultipleChoiceFilter(
        choices=Sprint.STATUS_CHOICES,
        lookup_expr='in'
    )
    
    # Project filter
    projeto = django_filters.ModelChoiceFilter(
        queryset=Projeto.objects.all(),
        field_name='projeto'
    )
    
    # Active sprints
    is_active = django_filters.BooleanFilter(method='filter_active')
    
    class Meta:
        model = Sprint
        fields = [
            'status', 'projeto', 'search', 'start_after', 'start_before',
            'end_after', 'end_before', 'is_active'
        ]
    
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
    
    def filter_active(self, queryset, name, value):
        """
        Filter active sprints (in progress and within date range).
        """
        from django.utils import timezone
        today = timezone.now().date()
        
        if value is True:
            return queryset.filter(
                status='em_andamento',
                data_inicio__lte=today,
                data_fim__gte=today
            )
        elif value is False:
            return queryset.exclude(
                status='em_andamento',
                data_inicio__lte=today,
                data_fim__gte=today
            )
        return queryset


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
        fields = ['papel', 'projeto', 'user_search']
    
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
