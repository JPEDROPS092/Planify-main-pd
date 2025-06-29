# tasks/filters.py

from django.utils import timezone
from django_filters.rest_framework import (
    FilterSet,
    CharFilter,
    DateFromToRangeFilter,
    BooleanFilter,
)

from .models import Tarefa


class TarefaFilter(FilterSet):
    """
    Filtro personalizado para o modelo Tarefa.

    Permite filtrar tarefas por diversos critérios como data, status, prioridade,
    responsáveis, e mais. Usado em conjunto com a TarefaViewSet.
    """

    titulo = CharFilter(
        lookup_expr="icontains",
        help_text="Filtra por parte do título (case-insensitive).",
    )
    descricao = CharFilter(
        lookup_expr="icontains",
        help_text="Filtra por parte da descrição (case-insensitive).",
    )

    # Filtros de data
    data_inicio_range = DateFromToRangeFilter(field_name="data_inicio")
    data_termino_range = DateFromToRangeFilter(field_name="data_termino")

    # Filtros baseados em métodos customizados
    status = CharFilter(
        method="filter_by_multiple_values",
        help_text="Filtra por status (pode ser um ou múltiplos, separados por vírgula).",
    )
    prioridade = CharFilter(
        method="filter_by_multiple_values",
        help_text="Filtra por prioridade (pode ser uma ou múltiplas, separadas por vírgula).",
    )
    responsavel_id = CharFilter(
        field_name="atribuicoes__usuario__id",
        lookup_expr="exact",
        help_text="Filtra tarefas por um ID de usuário responsável específico.",
    )
    sem_responsavel = BooleanFilter(
        field_name="atribuicoes",
        lookup_expr="isnull",
        help_text="Filtra tarefas sem responsáveis atribuídos.",
    )
    atrasada = BooleanFilter(
        method="filter_atrasada",
        help_text="Filtra tarefas atrasadas (data_termino < hoje e status não é 'FEITO').",
    )
    minhas_tarefas = BooleanFilter(
        method="filter_minhas_tarefas",
        help_text="Filtra apenas as tarefas atribuídas ao usuário autenticado.",
    )
    sem_sprint = BooleanFilter(
        field_name="sprint",
        lookup_expr="isnull",
        help_text="Filtra tarefas que não estão associadas a nenhuma sprint.",
    )

    class Meta:
        model = Tarefa
        fields = [
            "titulo",
            "descricao",
            "projeto",
            "sprint",
            "status",
            "prioridade",
            "data_inicio_range",
            "data_termino_range",
            "responsavel_id",
            "sem_responsavel",
            "atrasada",
            "minhas_tarefas",
            "sem_sprint",
        ]

    def filter_by_multiple_values(self, queryset, name, value):
        """
        Filtro genérico que aceita uma string de valores separados por vírgula
        e filtra o campo correspondente com `__in`.

        Ex: ?status=A_FAZER,EM_ANDAMENTO
        """
        values = [v.strip().upper() for v in value.split(",") if v.strip()]
        if not values:
            return queryset

        # O 'name' aqui será 'status' ou 'prioridade', dependendo de qual filtro o chamou.
        lookup = f"{name}__in"
        return queryset.filter(**{lookup: values})

    def filter_atrasada(self, queryset, name, value):
        """Filtra tarefas que estão atrasadas."""
        if value is True:
            return queryset.filter(data_termino__lt=timezone.now().date()).exclude(
                status="FEITO"
            )
        if value is False:
            return queryset.exclude(
                data_termino__lt=timezone.now().date(),
                status__in=["A_FAZER", "EM_ANDAMENTO"],
            )
        return queryset

    def filter_minhas_tarefas(self, queryset, name, value):
        """Filtra tarefas do usuário autenticado se o parâmetro for True."""
        request = getattr(self, "request", None)
        user = getattr(request, "user", None)
        if value and user and getattr(user, "is_authenticated", False):
            return queryset.filter(atribuicoes__usuario=user)
        return queryset

    def filter_sem_sprint(self, queryset, name, value):
        """Filtra tarefas que não estão associadas a nenhuma sprint."""
        if value:
            return queryset.filter(sprint__isnull=True)
        return queryset

    def filter_sem_responsavel(self, queryset, name, value):
        """Filtra tarefas que não têm responsáveis atribuídos."""
        if value:
            return queryset.filter(atribuicoes__isnull=True)
        return queryset
