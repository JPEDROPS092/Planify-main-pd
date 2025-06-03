from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

from .models import Projeto, MembroProjeto, Sprint
from tasks.models import Tarefa, AtribuicaoTarefa
from tasks.serializers import TarefaSerializer
from .api_schemas import TarefaCreateSerializer, TarefasBulkCreateSerializer, ErrorResponseSerializer

# Constants for task status values
STATUS_A_FAZER = 'A_FAZER'
STATUS_EM_ANDAMENTO = 'EM_ANDAMENTO'
STATUS_FEITO = 'FEITO'


@extend_schema(
    summary="Criar tarefa no projeto",
    description="Cria uma nova tarefa no contexto de um projeto específico",
    parameters=[
        OpenApiParameter(name='projeto_id', description='ID do projeto', required=True, type=int)
    ],
    request=TarefaCreateSerializer,
    responses={
        201: TarefaSerializer,
        400: ErrorResponseSerializer,
        403: ErrorResponseSerializer,
        404: ErrorResponseSerializer
    },
    tags=["Projetos", "Tarefas"]
)
class ProjetoTarefaCreateView(APIView):
    """
    View para criar tarefas diretamente a partir da visualização de um projeto.
    Permite criar tarefas rapidamente no contexto de Kanban ou Gantt.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, projeto_id):
        try:
            # Buscar o projeto pelo ID com select_related para otimizar consultas
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
                try:
                    # Usar get ao invés de get_object_or_404 para controle de erro mais específico
                    # Verificamos a existência do sprint mas não precisamos da variável
                    _ = Sprint.objects.get(id=sprint_id, projeto=projeto)
                except Sprint.DoesNotExist:
                    return Response(
                        {"detail": f"Sprint com ID {sprint_id} não existe neste projeto."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Validar os dados da tarefa
            serializer = TarefaSerializer(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Usar transação para garantir atomicidade na criação da tarefa e atribuições
            with transaction.atomic():
                # Salvar a tarefa com o usuário atual como criador
                tarefa = serializer.save(criado_por=request.user)
                
                # Atribuir responsáveis se especificados
                responsaveis = data.get('responsaveis', [])
                atribuicoes_criadas = []
                
                # Buscar todos os membros do projeto de uma vez para evitar consultas repetidas
                membros_ids = set(MembroProjeto.objects.filter(
                    projeto=projeto, 
                    usuario_id__in=responsaveis if responsaveis else [request.user.id]
                ).values_list('usuario_id', flat=True))
                
                for usuario_id in responsaveis:
                    # Verificar se o usuário é membro do projeto
                    if usuario_id in membros_ids:
                        atribuicao = AtribuicaoTarefa.objects.create(
                            tarefa=tarefa,
                            usuario_id=usuario_id,
                            atribuido_por=request.user
                        )
                        atribuicoes_criadas.append(atribuicao)
                
                # Se nenhum responsável foi especificado ou válido, atribuir ao criador
                if not atribuicoes_criadas:
                    AtribuicaoTarefa.objects.create(
                        tarefa=tarefa,
                        usuario=request.user,
                        atribuido_por=request.user
                    )
            
            # Buscar a tarefa com os responsáveis para retornar (otimizado)
            tarefa_completa = Tarefa.objects.select_related('projeto', 'sprint', 'criado_por').get(id=tarefa.id)
            responsaveis_data = AtribuicaoTarefa.objects.filter(tarefa=tarefa_completa).select_related('usuario').values(
                'usuario__id', 'usuario__username', 'usuario__full_name'
            )
            
            # Preparar resposta
            response_data = TarefaSerializer(tarefa_completa).data
            response_data['responsaveis'] = list(responsaveis_data)
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except (ValueError, TypeError, KeyError) as e:
            # Capturar erros específicos de validação ou dados
            return Response(
                {"detail": f"Erro de validação ao criar tarefa: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            # Capturar outros erros não tratados e registrar para debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erro não tratado ao criar tarefa: {str(e)}")
            return Response(
                {"detail": "Erro interno ao processar a solicitação. Por favor, contate o suporte."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    summary="Criar múltiplas tarefas no projeto",
    description="Cria múltiplas tarefas em lote no contexto de um projeto específico",
    parameters=[
        OpenApiParameter(name='projeto_id', description='ID do projeto', required=True, type=int)
    ],
    request=TarefasBulkCreateSerializer,
    responses={
        201: OpenApiTypes.OBJECT,
        207: OpenApiResponse(description="Criação parcial - algumas tarefas foram criadas com sucesso, outras falharam"),
        400: ErrorResponseSerializer,
        403: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
        500: ErrorResponseSerializer
    },
    tags=["Projetos", "Tarefas"]
)
class ProjetoTarefasBulkCreateView(APIView):
    """
    View para criar múltiplas tarefas de uma vez no contexto de um projeto.
    Útil para planejamento inicial ou criação de tarefas a partir de templates.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, projeto_id):
        try:
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
            
            # Pré-validar todas as tarefas e sprints antes de criar qualquer coisa
            sprints_ids = set(tarefa.get('sprint') for tarefa in tarefas_data if tarefa.get('sprint'))
            sprints_map = {}
            
            # Buscar todos os sprints de uma vez para evitar consultas repetidas
            if sprints_ids:
                sprints = Sprint.objects.filter(id__in=sprints_ids, projeto=projeto)
                sprints_map = {sprint.id: sprint for sprint in sprints}
            
            # Coletar todos os IDs de usuários para atribuição
            todos_responsaveis = set()
            for tarefa_data in tarefas_data:
                responsaveis = tarefa_data.get('responsaveis', [])
                if responsaveis:
                    todos_responsaveis.update(responsaveis)
                else:
                    todos_responsaveis.add(request.user.id)
            
            # Buscar todos os membros do projeto de uma vez
            membros_ids = set(MembroProjeto.objects.filter(
                projeto=projeto, 
                usuario_id__in=todos_responsaveis
            ).values_list('usuario_id', flat=True))
            
            # Lista para armazenar as tarefas criadas e erros
            tarefas_criadas = []
            erros = []
            
            # Usar transação para garantir atomicidade na criação de todas as tarefas
            with transaction.atomic():
                # Validar e criar cada tarefa
                for i, tarefa_data in enumerate(tarefas_data):
                    # Adicionar o projeto ao request.data
                    tarefa_data['projeto'] = projeto.id
                    
                    # Verificar se um sprint foi especificado
                    sprint_id = tarefa_data.get('sprint')
                    if sprint_id:
                        if sprint_id not in sprints_map:
                            erros.append({
                                'indice': i,
                                'erro': f"Sprint com ID {sprint_id} não existe neste projeto."
                            })
                            continue
                        # Adicionar o sprint ao contexto da tarefa (não usado diretamente, mas útil para logging/debugging)
                        _ = sprints_map[sprint_id]
                    
                    # Criar a tarefa
                    serializer = TarefaSerializer(data=tarefa_data)
                    if serializer.is_valid():
                        # Salvar a tarefa com o usuário atual como criador
                        tarefa = serializer.save(criado_por=request.user)
                        
                        # Atribuir responsáveis se especificados
                        responsaveis = tarefa_data.get('responsaveis', [])
                        atribuicoes_criadas = []
                        
                        for usuario_id in responsaveis:
                            # Verificar se o usuário é membro do projeto
                            if usuario_id in membros_ids:
                                atribuicao = AtribuicaoTarefa.objects.create(
                                    tarefa=tarefa,
                                    usuario_id=usuario_id,
                                    atribuido_por=request.user
                                )
                                atribuicoes_criadas.append(atribuicao)
                        
                        # Se nenhum responsável foi especificado ou válido, atribuir ao criador
                        if not atribuicoes_criadas:
                            AtribuicaoTarefa.objects.create(
                                tarefa=tarefa,
                                usuario=request.user,
                                atribuido_por=request.user
                            )
                        
                        # Adicionar à lista de tarefas criadas
                        tarefas_criadas.append(tarefa.id)
                    else:
                        erros.append({
                            'indice': i,
                            'erro': serializer.errors
                        })
                
                # Se houver erros e nenhuma tarefa criada, fazer rollback
                if erros and not tarefas_criadas:
                    # O rollback acontece automaticamente se uma exceção for lançada
                    raise ValueError("Nenhuma tarefa pôde ser criada devido a erros de validação.")
            
            # Buscar todas as tarefas criadas com seus relacionamentos para retornar
            if tarefas_criadas:
                tarefas_completas = Tarefa.objects.filter(id__in=tarefas_criadas).select_related(
                    'projeto', 'sprint', 'criado_por'
                )
                
                # Buscar todas as atribuições de uma vez
                atribuicoes = AtribuicaoTarefa.objects.filter(
                    tarefa__in=tarefas_completas
                ).select_related('usuario')
                
                # Agrupar atribuições por tarefa
                atribuicoes_por_tarefa = {}
                for atribuicao in atribuicoes:
                    if atribuicao.tarefa_id not in atribuicoes_por_tarefa:
                        atribuicoes_por_tarefa[atribuicao.tarefa_id] = []
                    atribuicoes_por_tarefa[atribuicao.tarefa_id].append({
                        'usuario__id': atribuicao.usuario.id,
                        'usuario__username': atribuicao.usuario.username,
                        'usuario__full_name': getattr(atribuicao.usuario, 'full_name', '')
                    })
                
                # Serializar tarefas com suas atribuições
                tarefas_serializadas = []
                for tarefa in tarefas_completas:
                    dados_tarefa = TarefaSerializer(tarefa).data
                    dados_tarefa['responsaveis'] = atribuicoes_por_tarefa.get(tarefa.id, [])
                    tarefas_serializadas.append(dados_tarefa)
                
                tarefas_criadas = tarefas_serializadas
            
            # Preparar resposta
            response_data = {
                'tarefas_criadas': tarefas_criadas,
                'total_criadas': len(tarefas_criadas),
                'erros': erros
            }
            
            if erros and tarefas_criadas:
                return Response(response_data, status=status.HTTP_207_MULTI_STATUS)
            elif tarefas_criadas:
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"detail": "Nenhuma tarefa foi criada devido a erros de validação.", "erros": erros},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except (ValueError, TypeError, KeyError) as e:
            # Capturar erros específicos de validação ou dados
            return Response(
                {"detail": f"Erro de validação ao criar tarefas em lote: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            # Capturar outros erros não tratados e registrar para debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erro não tratado ao criar tarefas em lote: {str(e)}")
            return Response(
                {"detail": "Erro interno ao processar a solicitação. Por favor, contate o suporte."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
