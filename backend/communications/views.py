from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils import timezone
# Removed unused import
from django.core.exceptions import ValidationError

from .models import ChatMensagem, ChatMensagemLeitura, Notificacao, ConfiguracaoNotificacao, Comunicacao
from .serializers import (
    ChatMensagemSerializer, ChatMensagemLeituraSerializer,
    NotificacaoSerializer, ConfiguracaoNotificacaoSerializer,
    ComunicacaoSerializer
)


class ChatMensagemViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de mensagens de chat.
    
    Permite criar, listar, atualizar e excluir mensagens de chat em projetos.
    Inclui funcionalidades para marcar mensagens como lidas e filtrar mensagens não lidas.
    
    Endpoints:
    - GET /chat-mensagens/ - Lista todas as mensagens (com filtros)
    - POST /chat-mensagens/ - Cria uma nova mensagem
    - GET /chat-mensagens/{id}/ - Obtém detalhes de uma mensagem
    - PUT/PATCH /chat-mensagens/{id}/ - Atualiza uma mensagem
    - DELETE /chat-mensagens/{id}/ - Remove uma mensagem
    - POST /chat-mensagens/{id}/marcar_como_lida/ - Marca uma mensagem como lida
    - GET /chat-mensagens/mensagens_nao_lidas/ - Lista mensagens não lidas
    """
    queryset = ChatMensagem.objects.select_related('projeto', 'autor').all()
    serializer_class = ChatMensagemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['projeto', 'autor']
    ordering_fields = ['enviado_em']
    
    def perform_create(self, serializer):
        """
        Sobrescreve o método para definir o autor como o usuário atual.
        
        Args:
            serializer: O serializer com os dados validados
        """
        serializer.save(autor=self.request.user)
    
    def get_queryset(self):
        """
        Filtra mensagens com base nos parâmetros da URL.
        
        Suporta os seguintes filtros:
        - projeto: ID do projeto
        - data_inicio: Data mínima de envio (formato YYYY-MM-DD)
        - data_fim: Data máxima de envio (formato YYYY-MM-DD)
        - texto: Texto contido na mensagem
        
        Returns:
            QuerySet: Mensagens filtradas com select_related para otimização
        """
        # Verifica se é uma chamada do Swagger para documentação
        if getattr(self, 'swagger_fake_view', False):
            return ChatMensagem.objects.none()
            
        # Inicia com select_related para otimizar consultas
        queryset = ChatMensagem.objects.select_related(
            'projeto', 'autor'
        ).prefetch_related(
            'leituras'
        )
        
        # Filtra por projeto
        projeto_id = self.request.GET.get('projeto')
        if projeto_id:
            try:
                projeto_id = int(projeto_id)
                queryset = queryset.filter(projeto_id=projeto_id)
            except (ValueError, TypeError):
                # Ignora filtro se o ID não for válido
                pass
        
        # Filtra por data
        data_inicio = self.request.GET.get('data_inicio')
        if data_inicio:
            queryset = queryset.filter(enviado_em__gte=data_inicio)
        
        data_fim = self.request.GET.get('data_fim')
        if data_fim:
            queryset = queryset.filter(enviado_em__lte=data_fim)
        
        # Filtra por texto
        texto = self.request.GET.get('texto')
        if texto:
            queryset = queryset.filter(texto__icontains=texto)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def marcar_como_lida(self, request, pk=None):  # noqa: Unused parameter
        """
        Marca uma mensagem como lida pelo usuário atual.
        
        Args:
            request: Objeto de requisição
            pk: ID da mensagem a ser marcada como lida
            
        Returns:
            Response: Detalhes do registro de leitura ou mensagem de status
        """
        try:
            mensagem = self.get_object()
            usuario = request.user
            
            # Verifica se já foi marcada como lida
            if ChatMensagemLeitura.objects.filter(mensagem=mensagem, usuario=usuario).exists():
                return Response(
                    {'mensagem': 'Esta mensagem já foi marcada como lida.'}, 
                    status=status.HTTP_200_OK
                )
            
            # Marca como lida
            leitura = ChatMensagemLeitura.objects.create(mensagem=mensagem, usuario=usuario)
            
            serializer = ChatMensagemLeituraSerializer(leitura)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'erro': f'Erro ao marcar mensagem como lida: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def mensagens_nao_lidas(self, request):
        """
        Retorna as mensagens não lidas pelo usuário atual.
        
        Suporta filtro por projeto através do parâmetro 'projeto' na query string.
        Exclui mensagens enviadas pelo próprio usuário, pois estas não precisam ser lidas.
        
        Args:
            request: Objeto de requisição
            
        Returns:
            Response: Lista de mensagens não lidas
        """
        usuario = request.user
        
        try:
            # Filtra por projeto, se fornecido
            projeto_id = request.query_params.get('projeto')
            filtro_projeto = Q()
            
            if projeto_id:
                try:
                    projeto_id = int(projeto_id)
                    filtro_projeto = Q(projeto_id=projeto_id)
                except (ValueError, TypeError):
                    # Ignora filtro se o ID não for válido
                    pass
            
            # Obtém IDs de mensagens já lidas pelo usuário
            mensagens_lidas = ChatMensagemLeitura.objects.filter(
                usuario=usuario
            ).values_list('mensagem_id', flat=True)
            
            # Filtra mensagens não lidas com select_related para otimização
            mensagens_nao_lidas = ChatMensagem.objects.select_related(
                'projeto', 'autor'
            ).filter(
                filtro_projeto
            ).exclude(
                id__in=mensagens_lidas
            ).exclude(
                autor=usuario  # Exclui mensagens enviadas pelo próprio usuário
            )
            
            serializer = self.get_serializer(mensagens_nao_lidas, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {'erro': f'Erro ao buscar mensagens não lidas: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class NotificacaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de notificações.
    
    Permite criar, listar, atualizar e excluir notificações do sistema.
    Inclui funcionalidades para marcar notificações como lidas e filtrar notificações não lidas.
    
    Endpoints:
    - GET /notificacoes/ - Lista notificações do usuário
    - GET /notificacoes/{id}/ - Obtém detalhes de uma notificação
    - POST /notificacoes/{id}/marcar_como_lida/ - Marca uma notificação como lida
    - POST /notificacoes/marcar_todas_como_lidas/ - Marca todas as notificações como lidas
    - GET /notificacoes/nao_lidas/ - Lista notificações não lidas
    """
    serializer_class = NotificacaoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['tipo', 'lida', 'prioridade', 'projeto', 'tarefa']
    ordering_fields = ['criada_em', 'prioridade']
    
    def get_queryset(self):
        """
        Retorna apenas as notificações do usuário atual.
        
        Otimiza a consulta com select_related para evitar consultas N+1.
        
        Returns:
            QuerySet: Notificações do usuário atual com relações otimizadas
        """
        if getattr(self, 'swagger_fake_view', False):
            # Retorna um queryset vazio para geração de esquema Swagger
            return Notificacao.objects.none()
            
        # Usa select_related para otimizar consultas relacionadas
        return Notificacao.objects.select_related(
            'usuario', 'projeto', 'tarefa'
        ).filter(usuario=self.request.user)
    
    @action(detail=True, methods=['post'])
    def marcar_como_lida(self, request, pk=None):
        """
        Marca uma notificação como lida.
        
        Define o campo 'lida' como True e registra a data/hora em 'lida_em'.
        
        Args:
            request: Objeto de requisição
            pk: ID da notificação a ser marcada como lida
            
        Returns:
            Response: Detalhes da notificação atualizada ou mensagem de status
        """
        try:
            notificacao = self.get_object()
            
            if notificacao.lida:
                return Response(
                    {'mensagem': 'Esta notificação já foi marcada como lida.'}, 
                    status=status.HTTP_200_OK
                )
            
            notificacao.lida = True
            notificacao.lida_em = timezone.now()
            notificacao.save(update_fields=['lida', 'lida_em'])  # Otimização: atualiza apenas campos necessários
            
            serializer = self.get_serializer(notificacao)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {'erro': f'Erro ao marcar notificação como lida: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'])
    def marcar_todas_como_lidas(self, request):
        """
        Marca todas as notificações não lidas do usuário como lidas.
        
        Atualiza em massa todas as notificações não lidas do usuário atual,
        definindo 'lida' como True e 'lida_em' como a data/hora atual.
        
        Args:
            request: Objeto de requisição
            
        Returns:
            Response: Mensagem de confirmação com o número de notificações atualizadas
        """
        try:
            # Filtra notificações não lidas do usuário atual
            notificacoes = Notificacao.objects.filter(usuario=request.user, lida=False)
            count = notificacoes.count()
            
            # Atualiza em massa (operação eficiente no banco de dados)
            notificacoes.update(lida=True, lida_em=timezone.now())
            
            return Response(
                {'mensagem': f'{count} notificações marcadas como lidas.'}, 
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {'erro': f'Erro ao marcar notificações como lidas: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def nao_lidas(self, request):
        """
        Retorna apenas as notificações não lidas do usuário.
        
        Suporta filtros adicionais por tipo e prioridade através de parâmetros na query string.
        
        Args:
            request: Objeto de requisição
            
        Returns:
            Response: Lista de notificações não lidas filtradas
        """
        try:
            # Inicia com select_related para otimizar consultas
            notificacoes = Notificacao.objects.select_related(
                'usuario', 'projeto', 'tarefa'
            ).filter(usuario=request.user, lida=False)
            
            # Filtra por tipo, se fornecido
            tipo = request.query_params.get('tipo')
            if tipo and tipo in dict(Notificacao.TIPO_CHOICES).keys():
                notificacoes = notificacoes.filter(tipo=tipo)
            
            # Filtra por prioridade, se fornecido
            prioridade = request.query_params.get('prioridade')
            if prioridade and prioridade in dict(Notificacao.PRIORIDADE_CHOICES).keys():
                notificacoes = notificacoes.filter(prioridade=prioridade)
                
            # Filtra por projeto, se fornecido
            projeto_id = request.query_params.get('projeto')
            if projeto_id:
                try:
                    projeto_id = int(projeto_id)
                    notificacoes = notificacoes.filter(projeto_id=projeto_id)
                except (ValueError, TypeError):
                    # Ignora filtro se o ID não for válido
                    pass
            
            serializer = self.get_serializer(notificacoes, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {'erro': f'Erro ao buscar notificações não lidas: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class ConfiguracaoNotificacaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de configurações de notificações.
    
    Permite criar, listar, atualizar e excluir configurações de notificações do usuário.
    Cada usuário pode ter suas próprias configurações para diferentes tipos de notificações.
    
    Endpoints:
    - GET /configuracoes-notificacao/ - Lista configurações do usuário
    - POST /configuracoes-notificacao/ - Cria uma nova configuração
    - GET /configuracoes-notificacao/{id}/ - Obtém detalhes de uma configuração
    - PUT/PATCH /configuracoes-notificacao/{id}/ - Atualiza uma configuração
    - DELETE /configuracoes-notificacao/{id}/ - Remove uma configuração
    """
    serializer_class = ConfiguracaoNotificacaoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Retorna apenas as configurações do usuário atual.
        
        Otimiza a consulta com select_related para evitar consultas N+1.
        
        Returns:
            QuerySet: Configurações de notificação do usuário atual
        """
        if getattr(self, 'swagger_fake_view', False):
            return ConfiguracaoNotificacao.objects.none()
            
        return ConfiguracaoNotificacao.objects.select_related('usuario').filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        """
        Define o usuário atual como proprietário da configuração.
        
        Verifica se já existe uma configuração para o tipo especificado antes de criar.
        
        Args:
            serializer: O serializer com os dados validados
            
        Raises:
            ValidationError: Se já existir uma configuração para o tipo especificado
        """
        tipo = serializer.validated_data.get('tipo')
        
        # Verifica se já existe uma configuração para este tipo
        if ConfiguracaoNotificacao.objects.filter(usuario=self.request.user, tipo=tipo).exists():
            raise ValidationError({
                'tipo': f'Já existe uma configuração para o tipo "{tipo}"'
            })
            
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


class ComunicacaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de comunicações formais.
    
    Permite criar, listar, atualizar e excluir comunicações formais em projetos.
    Comunicações formais são documentos oficiais como atas, memorandos e relatórios.
    
    Endpoints:
    - GET /comunicacoes/ - Lista todas as comunicações (com filtros)
    - POST /comunicacoes/ - Cria uma nova comunicação
    - GET /comunicacoes/{id}/ - Obtém detalhes de uma comunicação
    - PUT/PATCH /comunicacoes/{id}/ - Atualiza uma comunicação
    - DELETE /comunicacoes/{id}/ - Remove uma comunicação
    """
    serializer_class = ComunicacaoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['projeto', 'remetente', 'tipo']
    ordering_fields = ['criada_em', 'titulo']
    search_fields = ['titulo', 'texto']
    
    def get_queryset(self):
        """
        Retorna comunicações com base nos filtros aplicados.
        
        Otimiza a consulta com select_related para evitar consultas N+1.
        
        Returns:
            QuerySet: Comunicações filtradas com relações otimizadas
        """
        if getattr(self, 'swagger_fake_view', False):
            return Comunicacao.objects.none()
            
        # Inicia com select_related para otimizar consultas
        queryset = Comunicacao.objects.select_related(
            'projeto', 'remetente'
        )
        
        # Filtra por projeto
        projeto_id = self.request.GET.get('projeto')
        if projeto_id:
            try:
                projeto_id = int(projeto_id)
                queryset = queryset.filter(projeto_id=projeto_id)
            except (ValueError, TypeError):
                pass
                
        # Filtra por tipo
        tipo = self.request.GET.get('tipo')
        if tipo and tipo in dict(Comunicacao.TIPO_CHOICES).keys():
            queryset = queryset.filter(tipo=tipo)
                
        # Filtra por data
        data_inicio = self.request.GET.get('data_inicio')
        if data_inicio:
            queryset = queryset.filter(criada_em__gte=data_inicio)
        
        data_fim = self.request.GET.get('data_fim')
        if data_fim:
            queryset = queryset.filter(criada_em__lte=data_fim)
            
        return queryset
    
    def perform_create(self, serializer):
        """
        Define o remetente como o usuário atual ao criar uma nova comunicação.
        
        Args:
            serializer: O serializer com os dados validados
        """
        serializer.save(remetente=self.request.user)
        
    def update(self, request, *args, **kwargs):
        """
        Sobrescreve o método de atualização para verificar permissões.
        
        Apenas o remetente original ou um administrador pode atualizar uma comunicação.
        
        Args:
            request: Objeto de requisição
            
        Returns:
            Response: Resposta da atualização ou erro de permissão
        """
        comunicacao = self.get_object()
        
        # Verifica se o usuário é o remetente ou um administrador
        if request.user != comunicacao.remetente and not request.user.is_staff:
            return Response(
                {'erro': 'Você não tem permissão para editar esta comunicação.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        return super().update(request, *args, **kwargs)
