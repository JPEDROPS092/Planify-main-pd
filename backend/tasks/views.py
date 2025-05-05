from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Tarefa, AtribuicaoTarefa, ComentarioTarefa
from .serializers import (
    TarefaSerializer, TarefaListSerializer, AtribuicaoTarefaSerializer, 
    ComentarioTarefaSerializer, HistoricoStatusTarefaSerializer
)


class TarefaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de tarefas.
    Permite criar, listar, atualizar e excluir tarefas.
    """
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['projeto', 'sprint', 'status', 'prioridade']
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['data_inicio', 'data_termino', 'prioridade', 'criado_em', 'status']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TarefaListSerializer
        return TarefaSerializer
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)
    
    def get_queryset(self):
        """
        Filtra tarefas com base nos parâmetros da URL e permissões do usuário.
        """
        queryset = Tarefa.objects.all()
        
        # Filtra por usuário responsável
        usuario_id = self.request.query_params.get('usuario')
        if usuario_id:
            queryset = queryset.filter(atribuicoes__usuario__id=usuario_id)
        
        # Filtra por projeto
        projeto_id = self.request.query_params.get('projeto')
        if projeto_id:
            queryset = queryset.filter(projeto_id=projeto_id)
        
        # Filtra por sprint
        sprint_id = self.request.query_params.get('sprint')
        if sprint_id:
            if sprint_id == 'null':
                queryset = queryset.filter(sprint__isnull=True)
            else:
                queryset = queryset.filter(sprint_id=sprint_id)
        
        # Filtra por status
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        # Filtra por prioridade
        prioridade = self.request.query_params.get('prioridade')
        if prioridade:
            queryset = queryset.filter(prioridade=prioridade)
        
        # Filtra por texto (busca em título e descrição)
        texto = self.request.query_params.get('texto')
        if texto:
            queryset = queryset.filter(
                Q(titulo__icontains=texto) | Q(descricao__icontains=texto)
            )
        
        # Filtra minhas tarefas
        minhas_tarefas = self.request.query_params.get('minhas_tarefas')
        if minhas_tarefas and minhas_tarefas.lower() == 'true':
            queryset = queryset.filter(atribuicoes__usuario=self.request.user)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def atribuir_responsavel(self, request, pk=None):
        """
        Atribui um usuário como responsável pela tarefa.
        """
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
    
    @action(detail=True, methods=['post'])
    def remover_responsavel(self, request, pk=None):
        """
        Remove um usuário como responsável pela tarefa.
        """
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
    
    @action(detail=True, methods=['post'])
    def adicionar_comentario(self, request, pk=None):
        """
        Adiciona um comentário à tarefa.
        """
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
    
    @action(detail=True, methods=['post'])
    def associar_sprint(self, request, pk=None):
        """
        Associa a tarefa a uma sprint.
        """
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
    
    @action(detail=True, methods=['post'])
    def atualizar_status(self, request, pk=None):
        """
        Atualiza o status de uma tarefa.
        """
        tarefa = self.get_object()
        novo_status = request.data.get('status')
        
        if not novo_status:
            return Response(
                {'erro': 'É necessário fornecer um status.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verifica se o status é válido
        status_validos = dict(Tarefa.STATUS_CHOICES).keys()
        if novo_status not in status_validos:
            return Response(
                {'erro': f'Status inválido. Opções válidas: {", ".join(status_validos)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Atualiza o status
        status_antigo = tarefa.status
        tarefa.status = novo_status
        tarefa.save()
        
        # Retorna a tarefa atualizada
        serializer = self.get_serializer(tarefa)
        return Response(serializer.data)


class AtribuicaoTarefaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de atribuições de tarefas.
    """
    queryset = AtribuicaoTarefa.objects.all()
    serializer_class = AtribuicaoTarefaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tarefa', 'usuario']
    
    def perform_create(self, serializer):
        serializer.save(atribuido_por=self.request.user)


class ComentarioTarefaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de comentários de tarefas.
    """
    queryset = ComentarioTarefa.objects.all()
    serializer_class = ComentarioTarefaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tarefa', 'autor']
    
    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)
