"""
Filtros para o módulo de comunicações.

Este módulo centraliza toda a lógica de filtragem para as views de comunicações,
seguindo as melhores práticas do django-filters e mantendo o código DRY.
"""

import django_filters
from .models import ChatMensagem, Notificacao, Comunicacao


class ChatMensagemFilter(django_filters.FilterSet):
    """
    Filtros para mensagens de chat.
    
    Permite filtrar mensagens por:
    - Projeto
    - Autor
    - Período de envio (data_inicio e data_fim)
    - Conteúdo do texto (busca case-insensitive)
    """
    data_inicio = django_filters.DateFilter(
        field_name='enviado_em', 
        lookup_expr='gte',
        help_text='Data de início para filtrar mensagens (formato: YYYY-MM-DD)'
    )
    data_fim = django_filters.DateFilter(
        field_name='enviado_em', 
        lookup_expr='lte',
        help_text='Data de fim para filtrar mensagens (formato: YYYY-MM-DD)'
    )
    texto = django_filters.CharFilter(
        field_name='texto', 
        lookup_expr='icontains',
        help_text='Texto contido na mensagem (busca case-insensitive)'
    )

    class Meta:
        model = ChatMensagem
        fields = ['projeto', 'autor', 'data_inicio', 'data_fim', 'texto']


class ComunicacaoFilter(django_filters.FilterSet):
    """
    Filtros para comunicações formais.
    
    Permite filtrar comunicações por:
    - Projeto
    - Remetente
    - Tipo de comunicação
    - Período de criação (data_inicio e data_fim)
    - Conteúdo do título ou texto
    """
    data_inicio = django_filters.DateFilter(
        field_name='criada_em', 
        lookup_expr='gte',
        help_text='Data de início para filtrar comunicações (formato: YYYY-MM-DD)'
    )
    data_fim = django_filters.DateFilter(
        field_name='criada_em', 
        lookup_expr='lte',
        help_text='Data de fim para filtrar comunicações (formato: YYYY-MM-DD)'
    )
    titulo = django_filters.CharFilter(
        field_name='titulo', 
        lookup_expr='icontains',
        help_text='Texto contido no título da comunicação (busca case-insensitive)'
    )
    texto = django_filters.CharFilter(
        field_name='texto', 
        lookup_expr='icontains',
        help_text='Texto contido no conteúdo da comunicação (busca case-insensitive)'
    )

    class Meta:
        model = Comunicacao
        fields = ['projeto', 'remetente', 'tipo', 'data_inicio', 'data_fim', 'titulo', 'texto']


class NotificacaoFilter(django_filters.FilterSet):
    """
    Filtros para notificações com suporte ao GenericForeignKey.
    
    Permite filtrar notificações por:
    - Tipo
    - Status de leitura
    - Prioridade
    - Objeto relacionado (via content_type e object_id)
    - Período de criação
    """
    data_inicio = django_filters.DateFilter(
        field_name='criada_em', 
        lookup_expr='gte',
        help_text='Data de início para filtrar notificações (formato: YYYY-MM-DD)'
    )
    data_fim = django_filters.DateFilter(
        field_name='criada_em', 
        lookup_expr='lte',
        help_text='Data de fim para filtrar notificações (formato: YYYY-MM-DD)'
    )
    titulo = django_filters.CharFilter(
        field_name='titulo', 
        lookup_expr='icontains',
        help_text='Texto contido no título da notificação (busca case-insensitive)'
    )
    # Filtros para o GenericForeignKey
    content_type_model = django_filters.CharFilter(
        field_name='content_type__model',
        help_text='Filtrar por tipo de objeto relacionado (ex: projeto, tarefa)'
    )

    class Meta:
        model = Notificacao
        fields = [
            'tipo', 'lida', 'prioridade', 'data_inicio', 'data_fim', 'titulo',
            'content_type', 'object_id', 'content_type_model',
            # Manter campos legados para compatibilidade durante migração
            'projeto', 'tarefa'
        ]
