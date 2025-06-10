from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import ChatMensagem, ChatMensagemLeitura, Notificacao, ConfiguracaoNotificacao, Comunicacao
from .serializers import (
    ChatMensagemSerializer, ChatMensagemLeituraSerializer,
    NotificacaoSerializer, ConfiguracaoNotificacaoSerializer,
    ComunicacaoSerializer
)

@extend_schema_view(
    list=extend_schema(
        summary="Listar mensagens",
        description="Retorna todas as mensagens.",
        tags=['Communications']
    ),
    create=extend_schema(
        summary="Criar mensagem",
        description="Cria uma nova mensagem.",
        tags=['Communications']
    ),
    retrieve=extend_schema(
        summary="Obter mensagem",
        description="Retorna os detalhes de uma mensagem específica.",
        tags=['Communications']
    ),
    update=extend_schema(
        summary="Atualizar mensagem",
        description="Atualiza uma mensagem existente.",
        tags=['Communications']
    ),
    partial_update=extend_schema(
        summary="Atualizar mensagem parcialmente",
        description="Atualiza parcialmente uma mensagem.",
        tags=['Communications']
    ),
    destroy=extend_schema(
        summary="Excluir mensagem",
        description="Remove uma mensagem.",
        tags=['Communications']
    )
)
class ChatMensagemViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento de mensagens."""
    queryset = ChatMensagem.objects.select_related('projeto', 'autor').all()
    serializer_class = ChatMensagemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['projeto', 'autor']
    ordering_fields = ['enviado_em']
    
    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)

    @extend_schema(
        summary="Marcar como lida",
        description="Marca uma mensagem como lida pelo usuário atual.",
        tags=['Communications']
    )
    @action(detail=True, methods=['post'])
    def marcar_como_lida(self, request, pk=None):
        mensagem = self.get_object()
        ChatMensagemLeitura.objects.get_or_create(
            mensagem=mensagem,
            usuario=request.user
        )
        return Response({'status': 'mensagem marcada como lida'})

    @extend_schema(
        summary="Listar mensagens não lidas",
        description="Retorna todas as mensagens não lidas pelo usuário atual.",
        tags=['Communications']
    )
    @action(detail=False, methods=['get'])
    def mensagens_nao_lidas(self, request):
        mensagens = self.get_queryset().exclude(
            leituras__usuario=request.user
        )
        serializer = self.get_serializer(mensagens, many=True)
        return Response(serializer.data)

@extend_schema_view(
    list=extend_schema(tags=['Communications']),
    retrieve=extend_schema(tags=['Communications']),
    create=extend_schema(tags=['Communications']),
    update=extend_schema(tags=['Communications']),
    partial_update=extend_schema(tags=['Communications']),
    destroy=extend_schema(tags=['Communications'])
)
class NotificacaoViewSet(viewsets.ModelViewSet):
    queryset = Notificacao.objects.all()
    serializer_class = NotificacaoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(tags=['Communications'])
    @action(detail=True, methods=['post'])
    def marcar_como_lida(self, request, pk=None):
        notificacao = self.get_object()
        notificacao.lida = True
        notificacao.data_leitura = timezone.now()
        notificacao.save()
        return Response({'status': 'notificação marcada como lida'})

    @extend_schema(tags=['Communications'])
    @action(detail=False, methods=['post'])
    def marcar_todas_como_lidas(self, request):
        self.get_queryset().filter(usuario=request.user, lida=False).update(
            lida=True,
            data_leitura=timezone.now()
        )
        return Response({'status': 'todas notificações marcadas como lidas'})

    @extend_schema(tags=['Communications'])
    @action(detail=False, methods=['get'])
    def nao_lidas(self, request):
        notificacoes = self.get_queryset().filter(
            usuario=request.user,
            lida=False
        )
        serializer = self.get_serializer(notificacoes, many=True)
        return Response(serializer.data)

@extend_schema_view(
    list=extend_schema(tags=['Communications']),
    retrieve=extend_schema(tags=['Communications']),
    create=extend_schema(tags=['Communications']),
    update=extend_schema(tags=['Communications']),
    partial_update=extend_schema(tags=['Communications']),
    destroy=extend_schema(tags=['Communications'])
)
class ConfiguracaoNotificacaoViewSet(viewsets.ModelViewSet):
    queryset = ConfiguracaoNotificacao.objects.all()
    serializer_class = ConfiguracaoNotificacaoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(tags=['Communications'])
    @action(detail=False, methods=['get'])
    def minha_configuracao(self, request):
        configuracao = self.get_queryset().filter(usuario=request.user).first()
        if not configuracao:
            configuracao = ConfiguracaoNotificacao.objects.create(usuario=request.user)
        serializer = self.get_serializer(configuracao)
        return Response(serializer.data)
