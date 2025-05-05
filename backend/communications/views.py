from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils import timezone
from .models import ChatMensagem, ChatMensagemLeitura, Notificacao, ConfiguracaoNotificacao
from .serializers import (
    ChatMensagemSerializer, ChatMensagemLeituraSerializer,
    NotificacaoSerializer, ConfiguracaoNotificacaoSerializer
)


class ChatMensagemViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de mensagens de chat.
    Permite criar, listar, atualizar e excluir mensagens.
    """
    queryset = ChatMensagem.objects.all()
    serializer_class = ChatMensagemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['projeto', 'autor']
    ordering_fields = ['enviado_em']
    
    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)
    
    def get_queryset(self):
        """
        Filtra mensagens com base nos parâmetros da URL.
        """
        queryset = ChatMensagem.objects.all()
        
        # Filtra por projeto
        projeto_id = self.request.query_params.get('projeto')
        if projeto_id:
            queryset = queryset.filter(projeto_id=projeto_id)
        
        # Filtra por data
        data_inicio = self.request.query_params.get('data_inicio')
        if data_inicio:
            queryset = queryset.filter(enviado_em__gte=data_inicio)
        
        data_fim = self.request.query_params.get('data_fim')
        if data_fim:
            queryset = queryset.filter(enviado_em__lte=data_fim)
        
        # Filtra por texto
        texto = self.request.query_params.get('texto')
        if texto:
            queryset = queryset.filter(texto__icontains=texto)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def marcar_como_lida(self, request, pk=None):
        """
        Marca uma mensagem como lida pelo usuário atual.
        """
        mensagem = self.get_object()
        usuario = request.user
        
        # Verifica se já foi marcada como lida
        if ChatMensagemLeitura.objects.filter(mensagem=mensagem, usuario=usuario).exists():
            return Response({'mensagem': 'Esta mensagem já foi marcada como lida.'}, status=status.HTTP_200_OK)
        
        # Marca como lida
        leitura = ChatMensagemLeitura.objects.create(mensagem=mensagem, usuario=usuario)
        
        serializer = ChatMensagemLeituraSerializer(leitura)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def mensagens_nao_lidas(self, request):
        """
        Retorna as mensagens não lidas pelo usuário atual.
        """
        usuario = request.user
        
        # Filtra por projeto, se fornecido
        projeto_id = request.query_params.get('projeto')
        filtro_projeto = Q(projeto_id=projeto_id) if projeto_id else Q()
        
        # Obtém IDs de mensagens já lidas pelo usuário
        mensagens_lidas = ChatMensagemLeitura.objects.filter(usuario=usuario).values_list('mensagem_id', flat=True)
        
        # Filtra mensagens não lidas
        mensagens_nao_lidas = ChatMensagem.objects.filter(
            filtro_projeto
        ).exclude(
            id__in=mensagens_lidas
        ).exclude(
            autor=usuario  # Exclui mensagens enviadas pelo próprio usuário
        )
        
        serializer = self.get_serializer(mensagens_nao_lidas, many=True)
        return Response(serializer.data)


class NotificacaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de notificações.
    """
    serializer_class = NotificacaoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['tipo', 'lida', 'prioridade', 'projeto', 'tarefa']
    ordering_fields = ['criada_em', 'prioridade']
    
    def get_queryset(self):
        """
        Retorna apenas as notificações do usuário atual.
        """
        if getattr(self, 'swagger_fake_view', False):
            # Retorna um queryset vazio para geração de esquema Swagger
            return Notificacao.objects.none()
        return Notificacao.objects.filter(usuario=self.request.user)
    
    @action(detail=True, methods=['post'])
    def marcar_como_lida(self, request, pk=None):
        """
        Marca uma notificação como lida.
        """
        notificacao = self.get_object()
        
        if notificacao.lida:
            return Response({'mensagem': 'Esta notificação já foi marcada como lida.'}, status=status.HTTP_200_OK)
        
        notificacao.lida = True
        notificacao.lida_em = timezone.now()
        notificacao.save()
        
        serializer = self.get_serializer(notificacao)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def marcar_todas_como_lidas(self, request):
        """
        Marca todas as notificações do usuário como lidas.
        """
        notificacoes = Notificacao.objects.filter(usuario=request.user, lida=False)
        count = notificacoes.count()
        
        notificacoes.update(lida=True, lida_em=timezone.now())
        
        return Response({'mensagem': f'{count} notificações marcadas como lidas.'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def nao_lidas(self, request):
        """
        Retorna apenas as notificações não lidas do usuário.
        """
        notificacoes = Notificacao.objects.filter(usuario=request.user, lida=False)
        
        # Filtra por tipo, se fornecido
        tipo = request.query_params.get('tipo')
        if tipo:
            notificacoes = notificacoes.filter(tipo=tipo)
        
        # Filtra por prioridade, se fornecido
        prioridade = request.query_params.get('prioridade')
        if prioridade:
            notificacoes = notificacoes.filter(prioridade=prioridade)
        
        serializer = self.get_serializer(notificacoes, many=True)
        return Response(serializer.data)


class ConfiguracaoNotificacaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de configurações de notificações.
    """
    serializer_class = ConfiguracaoNotificacaoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Retorna apenas a configuração do usuário atual.
        """
        if getattr(self, 'swagger_fake_view', False):
            # Retorna um queryset vazio para geração de esquema Swagger
            return ConfiguracaoNotificacao.objects.none()
        return ConfiguracaoNotificacao.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        """
        Garante que a configuração seja criada para o usuário atual.
        """
        # Verifica se já existe configuração para o usuário
        try:
            config = ConfiguracaoNotificacao.objects.get(usuario=self.request.user)
            # Atualiza a configuração existente
            serializer.instance = config
            serializer.save()
        except ConfiguracaoNotificacao.DoesNotExist:
            # Cria nova configuração
            serializer.save(usuario=self.request.user)
    
    @action(detail=False, methods=['get'])
    def minha_configuracao(self, request):
        """
        Retorna a configuração do usuário atual ou cria uma padrão se não existir.
        """
        try:
            config = ConfiguracaoNotificacao.objects.get(usuario=request.user)
        except ConfiguracaoNotificacao.DoesNotExist:
            # Cria configuração padrão
            config = ConfiguracaoNotificacao.objects.create(usuario=request.user)
        
        serializer = self.get_serializer(config)
        return Response(serializer.data)
