from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Projeto, MembroProjeto, Sprint, HistoricoStatusProjeto
from .serializers import ProjetoSerializer, ProjetoListSerializer, MembroProjetoSerializer, SprintSerializer, HistoricoStatusProjetoSerializer
from tasks.models import Tarefa

User = get_user_model()

class ProjetoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de projetos.
    Permite criar, listar, atualizar e excluir projetos.
    """
    queryset = Projeto.objects.all()
    serializer_class = ProjetoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'prioridade', 'arquivado']
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['titulo', 'data_inicio', 'data_fim', 'criado_em', 'atualizado_em']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProjetoListSerializer
        return ProjetoSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def test_connection(self, request):
        """
        Endpoint para testar a conexão com a API.
        """
        return Response({'status': 'ok', 'message': 'API está funcionando corretamente!'})
    
    def perform_create(self, serializer):
        # Salva o projeto com o usuário atual como criador
        project = serializer.save(
            criado_por=self.request.user
        )
        
        # Adiciona o criador como membro do projeto com papel de gerente
        MembroProjeto.objects.create(
            projeto=project,
            usuario=self.request.user,
            papel='GERENTE'
        )
        
        # Registra a criação no histórico de status
        HistoricoStatusProjeto.objects.create(
            projeto=project,
            status_anterior='',
            novo_status=project.status,
            alterado_por=self.request.user
        )
    
    def perform_update(self, serializer):
        old_status = self.get_object().status
        project = serializer.save()
        
        # Se o status mudou, registra no histórico
        if old_status != project.status:
            HistoricoStatusProjeto.objects.create(
                projeto=project,
                status_anterior=old_status,
                novo_status=project.status,
                alterado_por=self.request.user
            )
    
    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        """
        Adiciona um membro ao projeto.
        """
        project = self.get_object()
        
        # Validação dos dados
        user_id = request.data.get('usuario')
        papel = request.data.get('papel', 'DESENVOLVEDOR')
        
        if not user_id:
            return Response(
                {'erro': 'ID do usuário é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verifica se o usuário já é membro
        if MembroProjeto.objects.filter(projeto=project, usuario_id=user_id).exists():
            return Response(
                {'erro': 'Usuário já é membro deste projeto'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(id=user_id)
            
            # Verifica se o papel é válido
            if papel not in dict(MembroProjeto.PAPEL_CHOICES).keys():
                return Response(
                    {'erro': f'Papel inválido. Escolha entre: {", ".join(dict(MembroProjeto.PAPEL_CHOICES).keys())}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            member = MembroProjeto.objects.create(
                projeto=project,
                usuario=user,
                papel=papel
            )
            
            serializer = MembroProjetoSerializer(member)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except User.DoesNotExist:
            return Response(
                {'erro': 'Usuário não encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        """
        Remove um membro do projeto.
        """
        project = self.get_object()
        user_id = request.data.get('usuario')
        
        if not user_id:
            return Response(
                {'erro': 'ID do usuário é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            member = MembroProjeto.objects.get(projeto=project, usuario_id=user_id)
            
            # Não permite remover o último gerente
            if member.papel == 'GERENTE' and MembroProjeto.objects.filter(projeto=project, papel='GERENTE').count() <= 1:
                return Response(
                    {'erro': 'Não é possível remover o último gerente do projeto'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            member.delete()
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


class SprintViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de sprints.
    Permite criar, listar, atualizar e excluir sprints.
    """
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['projeto', 'status']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['data_inicio', 'data_fim', 'criado_em']
    
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)
    
    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        """
        Lista as tarefas de um sprint.
        """
        sprint = self.get_object()
        tasks = Tarefa.objects.filter(sprint=sprint)
        
        from tasks.serializers import TarefaSerializer
        serializer = TarefaSerializer(tasks, many=True)
        
        return Response(serializer.data)
