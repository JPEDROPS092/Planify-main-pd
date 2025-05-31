from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import Projeto, MembroProjeto, Sprint
from tasks.models import Tarefa, AtribuicaoTarefa
from .serializers import ProjetoSerializer, SprintSerializer
from tasks.serializers import TarefaSerializer


class ProjetoDashboardView(APIView):
    """
    View para fornecer dados para o dashboard de um projeto específico,
    incluindo visualizações Kanban e Gantt.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, projeto_id):
        # Buscar o projeto pelo ID
        projeto = get_object_or_404(Projeto, id=projeto_id)
        
        # Verificar se o usuário tem acesso ao projeto
        if not MembroProjeto.objects.filter(projeto=projeto, usuario=request.user).exists() and not request.user.is_staff:
            return Response(
                {"detail": "Você não tem permissão para acessar este projeto."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Obter dados do projeto
        projeto_serializer = ProjetoSerializer(projeto)
        
        # Obter sprints do projeto
        sprints = Sprint.objects.filter(projeto=projeto)
        sprints_serializer = SprintSerializer(sprints, many=True)
        
        # Obter tarefas para o Kanban agrupadas por status
        tarefas_kanban = {
            'A_FAZER': [],
            'EM_ANDAMENTO': [],
            'FEITO': []
        }
        
        tarefas = Tarefa.objects.filter(projeto=projeto)
        for status in tarefas_kanban.keys():
            tarefas_status = tarefas.filter(status=status)
            tarefas_kanban[status] = TarefaSerializer(tarefas_status, many=True).data
        
        # Obter dados para o gráfico Gantt
        tarefas_gantt = []
        for tarefa in tarefas:
            responsaveis = AtribuicaoTarefa.objects.filter(tarefa=tarefa).values_list('usuario__username', flat=True)
            
            tarefa_gantt = {
                'id': tarefa.id,
                'titulo': tarefa.titulo,
                'inicio': tarefa.data_inicio.isoformat(),
                'fim': tarefa.data_termino.isoformat(),
                'progresso': 100 if tarefa.status == 'FEITO' else (50 if tarefa.status == 'EM_ANDAMENTO' else 0),
                'responsaveis': list(responsaveis),
                'status': tarefa.status,
                'prioridade': tarefa.prioridade
            }
            tarefas_gantt.append(tarefa_gantt)
        
        # Estatísticas do projeto
        total_tarefas = tarefas.count()
        tarefas_concluidas = tarefas.filter(status='FEITO').count()
        tarefas_em_andamento = tarefas.filter(status='EM_ANDAMENTO').count()
        tarefas_a_fazer = tarefas.filter(status='A_FAZER').count()
        
        # Calcular progresso geral do projeto
        progresso = 0
        if total_tarefas > 0:
            progresso = (tarefas_concluidas / total_tarefas) * 100
        
        # Verificar se o projeto está atrasado
        hoje = timezone.now().date()
        tarefas_atrasadas = tarefas.filter(
            status__in=['A_FAZER', 'EM_ANDAMENTO'],
            data_termino__lt=hoje
        ).count()
        
        # Próximos prazos
        proximos_prazos = tarefas.filter(
            status__in=['A_FAZER', 'EM_ANDAMENTO'],
            data_termino__gte=hoje,
            data_termino__lte=hoje + timedelta(days=7)
        ).order_by('data_termino')
        
        proximos_prazos_data = TarefaSerializer(proximos_prazos, many=True).data
        
        # Membros do projeto
        membros = MembroProjeto.objects.filter(projeto=projeto)
        membros_data = []
        for membro in membros:
            tarefas_membro = tarefas.filter(atribuicoes__usuario=membro.usuario).count()
            tarefas_concluidas_membro = tarefas.filter(
                atribuicoes__usuario=membro.usuario,
                status='FEITO'
            ).count()
            
            membros_data.append({
                'id': membro.usuario.id,
                'username': membro.usuario.username,
                'nome_completo': membro.usuario.full_name,
                'papel': membro.papel,
                'tarefas_total': tarefas_membro,
                'tarefas_concluidas': tarefas_concluidas_membro
            })
        
        # Montar resposta completa
        response_data = {
            'projeto': projeto_serializer.data,
            'sprints': sprints_serializer.data,
            'kanban': tarefas_kanban,
            'gantt': tarefas_gantt,
            'estatisticas': {
                'total_tarefas': total_tarefas,
                'tarefas_concluidas': tarefas_concluidas,
                'tarefas_em_andamento': tarefas_em_andamento,
                'tarefas_a_fazer': tarefas_a_fazer,
                'tarefas_atrasadas': tarefas_atrasadas,
                'progresso': progresso
            },
            'proximos_prazos': proximos_prazos_data,
            'membros': membros_data
        }
        
        return Response(response_data)


class ProjetoKanbanView(APIView):
    """
    View específica para fornecer dados para a visualização Kanban de um projeto.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, projeto_id):
        # Buscar o projeto pelo ID
        projeto = get_object_or_404(Projeto, id=projeto_id)
        
        # Verificar se o usuário tem acesso ao projeto
        if not MembroProjeto.objects.filter(projeto=projeto, usuario=request.user).exists() and not request.user.is_staff:
            return Response(
                {"detail": "Você não tem permissão para acessar este projeto."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Obter tarefas agrupadas por status
        tarefas_kanban = {
            'A_FAZER': [],
            'EM_ANDAMENTO': [],
            'FEITO': []
        }
        
        # Filtrar por sprint se especificado
        sprint_id = request.query_params.get('sprint')
        tarefas_query = Tarefa.objects.filter(projeto=projeto)
        
        if sprint_id:
            if sprint_id == 'null':
                tarefas_query = tarefas_query.filter(sprint__isnull=True)
            else:
                tarefas_query = tarefas_query.filter(sprint_id=sprint_id)
        
        for status in tarefas_kanban.keys():
            tarefas_status = tarefas_query.filter(status=status)
            tarefas_serialized = []
            
            for tarefa in tarefas_status:
                # Obter responsáveis pela tarefa
                responsaveis = AtribuicaoTarefa.objects.filter(tarefa=tarefa).values(
                    'usuario__id', 'usuario__username', 'usuario__full_name'
                )
                
                tarefa_data = TarefaSerializer(tarefa).data
                tarefa_data['responsaveis'] = list(responsaveis)
                tarefas_serialized.append(tarefa_data)
            
            tarefas_kanban[status] = tarefas_serialized
        
        return Response(tarefas_kanban)
    
    def patch(self, request, projeto_id):
        """
        Atualiza o status de uma tarefa (para arrastar e soltar no Kanban)
        """
        # Buscar o projeto pelo ID
        projeto = get_object_or_404(Projeto, id=projeto_id)
        
        # Verificar se o usuário tem acesso ao projeto
        if not MembroProjeto.objects.filter(projeto=projeto, usuario=request.user).exists() and not request.user.is_staff:
            return Response(
                {"detail": "Você não tem permissão para acessar este projeto."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        tarefa_id = request.data.get('tarefa_id')
        novo_status = request.data.get('status')
        
        if not tarefa_id or not novo_status:
            return Response(
                {"detail": "ID da tarefa e novo status são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar se o status é válido
        if novo_status not in dict(Tarefa.STATUS_CHOICES):
            return Response(
                {"detail": f"Status inválido. Opções válidas: {dict(Tarefa.STATUS_CHOICES).keys()}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Buscar a tarefa
        try:
            tarefa = Tarefa.objects.get(id=tarefa_id, projeto=projeto)
        except Tarefa.DoesNotExist:
            return Response(
                {"detail": "Tarefa não encontrada neste projeto."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Salvar o status anterior
        status_anterior = tarefa.status
        
        # Atualizar o status
        tarefa.status = novo_status
        tarefa.save()
        
        # Registrar mudança no histórico
        tarefa.historico_status.create(
            status_anterior=status_anterior,
            novo_status=novo_status,
            alterado_por=request.user
        )
        
        return Response({"detail": "Status atualizado com sucesso."})


class ProjetoGanttView(APIView):
    """
    View específica para fornecer dados para a visualização Gantt de um projeto.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, projeto_id):
        # Buscar o projeto pelo ID
        projeto = get_object_or_404(Projeto, id=projeto_id)
        
        # Verificar se o usuário tem acesso ao projeto
        if not MembroProjeto.objects.filter(projeto=projeto, usuario=request.user).exists() and not request.user.is_staff:
            return Response(
                {"detail": "Você não tem permissão para acessar este projeto."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Filtrar por sprint se especificado
        sprint_id = request.query_params.get('sprint')
        tarefas_query = Tarefa.objects.filter(projeto=projeto)
        
        if sprint_id:
            if sprint_id == 'null':
                tarefas_query = tarefas_query.filter(sprint__isnull=True)
            else:
                tarefas_query = tarefas_query.filter(sprint_id=sprint_id)
        
        # Obter dados para o gráfico Gantt
        tarefas_gantt = []
        for tarefa in tarefas_query:
            responsaveis = AtribuicaoTarefa.objects.filter(tarefa=tarefa).values(
                'usuario__id', 'usuario__username', 'usuario__full_name'
            )
            
            tarefa_gantt = {
                'id': tarefa.id,
                'titulo': tarefa.titulo,
                'inicio': tarefa.data_inicio.isoformat(),
                'fim': tarefa.data_termino.isoformat(),
                'progresso': 100 if tarefa.status == 'FEITO' else (50 if tarefa.status == 'EM_ANDAMENTO' else 0),
                'responsaveis': list(responsaveis),
                'status': tarefa.status,
                'prioridade': tarefa.prioridade,
                'descricao': tarefa.descricao
            }
            tarefas_gantt.append(tarefa_gantt)
        
        # Adicionar sprints ao Gantt se houver
        sprints = Sprint.objects.filter(projeto=projeto)
        sprints_gantt = []
        
        for sprint in sprints:
            sprint_gantt = {
                'id': f"sprint_{sprint.id}",
                'titulo': f"Sprint: {sprint.nome}",
                'inicio': sprint.data_inicio.isoformat(),
                'fim': sprint.data_fim.isoformat(),
                'tipo': 'sprint',
                'progresso': 100 if sprint.status == 'CONCLUIDO' else (
                    50 if sprint.status == 'EM_ANDAMENTO' else 0
                ),
                'status': sprint.status
            }
            sprints_gantt.append(sprint_gantt)
        
        # Adicionar o próprio projeto ao Gantt
        projeto_gantt = {
            'id': f"projeto_{projeto.id}",
            'titulo': f"Projeto: {projeto.titulo}",
            'inicio': projeto.data_inicio.isoformat(),
            'fim': projeto.data_fim.isoformat(),
            'tipo': 'projeto',
            'progresso': 100 if projeto.status == 'CONCLUIDO' else (
                50 if projeto.status == 'EM_ANDAMENTO' else 0
            ),
            'status': projeto.status
        }
        
        # Combinar todos os dados
        gantt_data = {
            'projeto': projeto_gantt,
            'sprints': sprints_gantt,
            'tarefas': tarefas_gantt
        }
        
        return Response(gantt_data)
