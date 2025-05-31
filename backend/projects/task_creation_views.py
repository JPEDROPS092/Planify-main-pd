from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Projeto, MembroProjeto, Sprint
from tasks.models import Tarefa, AtribuicaoTarefa
from tasks.serializers import TarefaSerializer


class ProjetoTarefaCreateView(APIView):
    """
    View para criar tarefas diretamente a partir da visualização de um projeto.
    Permite criar tarefas rapidamente no contexto de Kanban ou Gantt.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, projeto_id):
        # Buscar o projeto pelo ID
        projeto = get_object_or_404(Projeto, id=projeto_id)
        
        # Verificar se o usuário tem acesso ao projeto
        if not MembroProjeto.objects.filter(projeto=projeto, usuario=request.user).exists() and not request.user.is_staff:
            return Response(
                {"detail": "Você não tem permissão para acessar este projeto."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Adicionar o projeto ao request.data
        data = request.data.copy()
        data['projeto'] = projeto.id
        
        # Verificar se um sprint foi especificado
        sprint_id = data.get('sprint')
        if sprint_id:
            # Verificar se o sprint existe e pertence ao projeto
            sprint = get_object_or_404(Sprint, id=sprint_id, projeto=projeto)
        
        # Criar a tarefa
        serializer = TarefaSerializer(data=data)
        if serializer.is_valid():
            # Salvar a tarefa com o usuário atual como criador
            tarefa = serializer.save(criado_por=request.user)
            
            # Atribuir responsáveis se especificados
            responsaveis = data.get('responsaveis', [])
            for usuario_id in responsaveis:
                # Verificar se o usuário é membro do projeto
                if MembroProjeto.objects.filter(projeto=projeto, usuario_id=usuario_id).exists():
                    AtribuicaoTarefa.objects.create(
                        tarefa=tarefa,
                        usuario_id=usuario_id,
                        atribuido_por=request.user
                    )
            
            # Se nenhum responsável foi especificado, atribuir ao criador
            if not responsaveis:
                AtribuicaoTarefa.objects.create(
                    tarefa=tarefa,
                    usuario=request.user,
                    atribuido_por=request.user
                )
            
            # Buscar a tarefa com os responsáveis para retornar
            tarefa_completa = Tarefa.objects.get(id=tarefa.id)
            responsaveis_data = AtribuicaoTarefa.objects.filter(tarefa=tarefa_completa).values(
                'usuario__id', 'usuario__username', 'usuario__full_name'
            )
            
            # Preparar resposta
            response_data = TarefaSerializer(tarefa_completa).data
            response_data['responsaveis'] = list(responsaveis_data)
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjetoTarefasBulkCreateView(APIView):
    """
    View para criar múltiplas tarefas de uma vez no contexto de um projeto.
    Útil para planejamento inicial ou criação de tarefas a partir de templates.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, projeto_id):
        # Buscar o projeto pelo ID
        projeto = get_object_or_404(Projeto, id=projeto_id)
        
        # Verificar se o usuário tem acesso ao projeto
        if not MembroProjeto.objects.filter(projeto=projeto, usuario=request.user).exists() and not request.user.is_staff:
            return Response(
                {"detail": "Você não tem permissão para acessar este projeto."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Obter a lista de tarefas do request
        tarefas_data = request.data.get('tarefas', [])
        if not tarefas_data:
            return Response(
                {"detail": "Nenhuma tarefa fornecida."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Lista para armazenar as tarefas criadas
        tarefas_criadas = []
        erros = []
        
        # Criar cada tarefa
        for i, tarefa_data in enumerate(tarefas_data):
            # Adicionar o projeto ao request.data
            tarefa_data['projeto'] = projeto.id
            
            # Verificar se um sprint foi especificado
            sprint_id = tarefa_data.get('sprint')
            if sprint_id:
                # Verificar se o sprint existe e pertence ao projeto
                try:
                    sprint = Sprint.objects.get(id=sprint_id, projeto=projeto)
                except Sprint.DoesNotExist:
                    erros.append({
                        'indice': i,
                        'erro': f"Sprint com ID {sprint_id} não existe neste projeto."
                    })
                    continue
            
            # Criar a tarefa
            serializer = TarefaSerializer(data=tarefa_data)
            if serializer.is_valid():
                # Salvar a tarefa com o usuário atual como criador
                tarefa = serializer.save(criado_por=request.user)
                
                # Atribuir responsáveis se especificados
                responsaveis = tarefa_data.get('responsaveis', [])
                for usuario_id in responsaveis:
                    # Verificar se o usuário é membro do projeto
                    if MembroProjeto.objects.filter(projeto=projeto, usuario_id=usuario_id).exists():
                        AtribuicaoTarefa.objects.create(
                            tarefa=tarefa,
                            usuario_id=usuario_id,
                            atribuido_por=request.user
                        )
                
                # Se nenhum responsável foi especificado, atribuir ao criador
                if not responsaveis:
                    AtribuicaoTarefa.objects.create(
                        tarefa=tarefa,
                        usuario=request.user,
                        atribuido_por=request.user
                    )
                
                # Adicionar à lista de tarefas criadas
                tarefas_criadas.append(TarefaSerializer(tarefa).data)
            else:
                erros.append({
                    'indice': i,
                    'erro': serializer.errors
                })
        
        # Preparar resposta
        response_data = {
            'tarefas_criadas': tarefas_criadas,
            'total_criadas': len(tarefas_criadas),
            'erros': erros
        }
        
        if erros:
            return Response(response_data, status=status.HTTP_207_MULTI_STATUS)
        
        return Response(response_data, status=status.HTTP_201_CREATED)
