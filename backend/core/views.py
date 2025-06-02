from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

# Imports adicionados para drf-spectacular e serializadores
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers

from projects.models import Projeto
from tasks.models import Tarefa
from risks.models import Risco
from costs.models import Custo
from .decorators import swagger_schema_with_examples
from .openapi import dashboard_schema, health_check_schema

# Serializers para drf-spectacular
# Comentário: Serializadores para definir os esquemas de resposta para drf-spectacular.
# Estes serializadores ajudam a gerar uma documentação da API clara e precisa.

class TarefaStatusCountSerializer(serializers.Serializer):
    # Comentário: Representa a contagem de tarefas para um status específico.
    status = serializers.CharField(help_text="Status da tarefa (ex: Pendente, Em Andamento, Concluída)")
    count = serializers.IntegerField(help_text="Quantidade de tarefas com este status")

class VisaoGeralDashboardSerializer(serializers.Serializer):
    # Comentário: Define a estrutura dos dados para a visão geral do dashboard.
    total_projetos = serializers.IntegerField(help_text="Número total de projetos no sistema")
    total_tarefas = serializers.IntegerField(help_text="Número total de tarefas no sistema")
    tarefas_por_status = TarefaStatusCountSerializer(many=True, help_text="Lista detalhada da contagem de tarefas por cada status")

class MetricasProjetoSerializer(serializers.Serializer):
    # Comentário: Define a estrutura dos dados para as métricas de um projeto específico.
    tarefas_por_status = TarefaStatusCountSerializer(many=True, help_text="Contagem de tarefas do projeto, agrupadas por status")
    progresso = serializers.FloatField(help_text="Percentual de conclusão do projeto (0-100)")
    riscos_ativos = serializers.IntegerField(help_text="Número de riscos atualmente ativos para o projeto")
    custos_totais = serializers.FloatField(help_text="Soma dos custos registrados para o projeto")
    dias_restantes = serializers.IntegerField(help_text="Número de dias restantes até a data final planejada do projeto")

class ErrorSerializer(serializers.Serializer):
    # Comentário: Serializador padrão para respostas de erro.
    error = serializers.CharField(help_text="Mensagem descrevendo o erro ocorrido")

class ProximaTarefaSerializer(serializers.Serializer):
    # Comentário: Define a estrutura para os detalhes de uma próxima tarefa.
    titulo = serializers.CharField(help_text="Título da tarefa")
    data_inicio = serializers.DateTimeField(help_text="Data e hora de início planejadas para a tarefa")
    projeto__titulo = serializers.CharField(help_text="Título do projeto ao qual esta tarefa pertence")

class DashboardUsuarioSerializer(serializers.Serializer):
    # Comentário: Define a estrutura dos dados para o dashboard pessoal do usuário.
    projetos_gerenciados = serializers.IntegerField(help_text="Número de projetos onde o usuário é o gerente")
    tarefas_por_status = TarefaStatusCountSerializer(many=True, help_text="Contagem das tarefas do usuário, agrupadas por status")
    tarefas_atrasadas = serializers.IntegerField(help_text="Número de tarefas atribuídas ao usuário que estão atrasadas")
    proximas_tarefas = ProximaTarefaSerializer(many=True, help_text="Lista das próximas tarefas agendadas para o usuário")

@extend_schema(
    exclude=True,  # Comentário: Esta view é um redirecionamento, não precisa aparecer na documentação da API.
    tags=['Outros'] 
)
@api_view(['GET'])
@permission_classes([AllowAny])
def documentacao_api(request):
    """
    Redireciona para a documentação da API.
    """
    return redirect('openapi-schema')

@extend_schema(
    operation_id='health_check_retrieve',
    summary="Verificação de Saúde Simples",
    description="Endpoint simples para verificar se a API está operacional. Retorna 'ok' se estiver tudo certo.",
    responses={
        200: OpenApiResponse(
            response={'type': 'object', 'properties': {'status': {'type': 'string', 'example': 'ok'}}},
            description="API está operacional."
        )
    },
    tags=['Saúde do Sistema']
)
@api_view(['GET'])
@permission_classes([AllowAny])
@extend_schema(
    summary="Verificar status da API",
    description="Endpoint para verificar se a API está funcionando corretamente",
    responses={200: OpenApiTypes.OBJECT},
    examples=[
        OpenApiExample(
            'Exemplo de resposta',
            value={
                'status': 'ok',
                'database': 'connected',
                'version': '1.0.0'
            }
        )
    ]
)
def checagem_saude(request):
    """
    Endpoint para verificar se a API está funcionando
    """
    return Response({"status": "ok"})

@extend_schema(
    operation_id='health_check_original_retrieve',
    summary="Verificação de Saúde Detalhada",
    description="Endpoint para verificar o estado da API, incluindo versão e ambiente. Não requer autenticação.",
    responses={
        200: OpenApiResponse(
            response={
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'online'},
                    'versao': {'type': 'string', 'example': '1.0'},
                    'ambiente': {'type': 'string', 'example': 'desenvolvimento'},
                    'data_hora': {'type': 'string', 'format': 'date-time', 'example': '2024-07-15T14:30:00Z'}
                }
            },
            description="API está operacional com detalhes."
        )
    },
    tags=['Saúde do Sistema']
)
@api_view(['GET'])
@permission_classes([AllowAny])
@extend_schema(
    summary="Verificar status da API (versão original)",
    description="Endpoint simples para verificar se a API está funcionando. Não requer autenticação.",
    responses={200: OpenApiTypes.OBJECT},
    examples=[
        OpenApiExample(
            'Exemplo de resposta',
            value={
                'status': 'ok'
            }
        )
    ]
)
def checagem_saude_original(request):
    """
    Endpoint simples para verificar se a API está funcionando.
    Não requer autenticação.
    """
    return Response({
        "status": "online",
        "versao": "1.0",
        "ambiente": "desenvolvimento",
        "data_hora": timezone.now().isoformat()
    })

# Aliases para manter compatibilidade com código existente
api_documentation = documentacao_api
health_check = checagem_saude
health_check_original = checagem_saude_original

@extend_schema(
    operation_id='visao_geral_dashboard_retrieve',
    summary="Visão Geral do Dashboard",
    description="Retorna uma visão geral do sistema, incluindo o número total de projetos, tarefas e a distribuição de tarefas por status. Requer autenticação.",
    responses={
        200: OpenApiResponse(
            response=VisaoGeralDashboardSerializer,
            description="Dados consolidados do dashboard.",
            examples=[
                OpenApiExample(
                    name="Exemplo de Resposta",
                    summary="Exemplo de dados retornados pelo dashboard.",
                    value={
                        'total_projetos': 5,
                        'total_tarefas': 15,
                        'tarefas_por_status': [
                            {'status': 'Pendente', 'count': 5},
                            {'status': 'Em Andamento', 'count': 7},
                            {'status': 'Concluída', 'count': 3}
                        ]
                    }
                )
            ]
        )
    },
    tags=['Dashboard']
)
@api_view(['GET'])
@extend_schema(
    summary="Visão geral do dashboard",
    description="Endpoint para obter dados gerais do dashboard",
    responses={
        200: VisaoGeralDashboardSerializer,
        400: ErrorSerializer,
        401: ErrorSerializer
    }
)
def visao_geral_dashboard(request):
    """
    Endpoint para obter dados do dashboard
    """
    total_projetos = Projeto.objects.count()
    total_tarefas = Tarefa.objects.count()
    tarefas_por_status = Tarefa.objects.values('status').annotate(count=Count('id'))
    
    # Converter os status para nomes mais amigáveis
    status_map = {
        'A_FAZER': 'Pendente',
        'EM_ANDAMENTO': 'Em Andamento',
        'FEITO': 'Concluída',
        'BLOQUEADA': 'Bloqueada',
        'CANCELADA': 'Cancelada'
    }
    
    tarefas_por_status_formatted = [
        {'status': status_map.get(item['status'], item['status']), 'count': item['count']}
        for item in tarefas_por_status
    ]
    
    data = {
        'total_projetos': total_projetos,
        'total_tarefas': total_tarefas,
        'tarefas_por_status': tarefas_por_status_formatted
    }
    return Response(data)

dashboard_overview = visao_geral_dashboard

@extend_schema(
    operation_id='metricas_projeto_retrieve',
    summary="Métricas Detalhadas do Projeto",
    description="Fornece métricas detalhadas para um projeto específico, como distribuição de tarefas por status, progresso, riscos ativos, custos e dias restantes. Acessível publicamente para fins de demonstração ou integração externa.",
    parameters=[
        OpenApiParameter(
            name='project_id',
            location=OpenApiParameter.PATH,
            description="ID numérico do projeto para o qual as métricas são solicitadas.",
            required=True,
            type=OpenApiTypes.INT 
        )
    ],
    responses={
        200: OpenApiResponse(
            response=MetricasProjetoSerializer,
            description="Métricas detalhadas do projeto.",
            examples=[
                OpenApiExample(
                    name="Exemplo de Métricas",
                    summary="Exemplo de métricas retornadas para um projeto.",
                    value={
                        'tarefas_por_status': [
                            {'status': 'Pendente', 'count': 5},
                            {'status': 'Em Andamento', 'count': 3},
                            {'status': 'Concluída', 'count': 7}
                        ],
                        'progresso': 46.67,
                        'riscos_ativos': 2,
                        'custos_totais': 15000.0,
                        'dias_restantes': 30
                    }
                )
            ]
        ),
        404: OpenApiResponse(
            response=ErrorSerializer,
            description="O projeto com o ID especificado não foi encontrado.",
            examples=[
                OpenApiExample(
                    name="Erro Projeto Não Encontrado",
                    summary="Exemplo de erro quando o projeto não é encontrado.",
                    value={"error": "Projeto não encontrado"}
                )
            ]
        )
    },
    tags=['Projetos', 'Dashboard']
)
@api_view(['GET'])
@permission_classes([AllowAny]) # Mantido conforme original
@extend_schema(
    summary="Métricas de projeto",
    description="Retorna métricas específicas de um projeto",
    parameters=[
        OpenApiParameter(name='project_id', description='ID do projeto', required=True, type=int)
    ],
    responses={
        200: MetricasProjetoSerializer,
        400: ErrorSerializer,
        401: ErrorSerializer,
        404: ErrorSerializer
    }
)
def metricas_projeto(request, project_id):
    """
    Retorna métricas específicas de um projeto.
    """
    try:
        projeto = Projeto.objects.get(id=project_id)
    except Projeto.DoesNotExist:
        return Response(
            {"error": "Projeto não encontrado"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Tarefas do projeto por status
    tarefas = Tarefa.objects.filter(projeto=projeto)
    tarefas_por_status = tarefas.values('status').annotate(count=Count('id'))
    
    # Progresso do projeto (% de tarefas concluídas)
    total_tarefas = tarefas.count()
    tarefas_concluidas = tarefas.filter(status='FEITO').count()
    progresso = (tarefas_concluidas / total_tarefas * 100) if total_tarefas > 0 else 0
    
    # Riscos ativos
    riscos_ativos = Risco.objects.filter(
        projeto=projeto,
        status__in=['IDENTIFICADO', 'EM_ANALISE']
    ).count()
    
    # Custos totais
    custos_totais = Custo.objects.filter(projeto=projeto).aggregate(total=Sum('valor'))
    
    # Dias restantes
    dias_restantes = (projeto.data_fim - timezone.now()).days if projeto.data_fim > timezone.now() else 0
    
    # Converter os status para nomes mais amigáveis
    status_map = {
        'A_FAZER': 'Pendente',
        'EM_ANDAMENTO': 'Em Andamento',
        'FEITO': 'Concluída',
        'BLOQUEADA': 'Bloqueada',
        'CANCELADA': 'Cancelada'
    }
    
    tarefas_por_status_formatted = [
        {'status': status_map.get(item['status'], item['status']), 'count': item['count']}
        for item in tarefas_por_status
    ]
    
    return Response({
        'tarefas_por_status': tarefas_por_status_formatted,
        'progresso': progresso,
        'riscos_ativos': riscos_ativos,
        'custos_totais': custos_totais['total'] or 0,
        'dias_restantes': dias_restantes
    })

project_metrics = metricas_projeto

@extend_schema(
    operation_id='dashboard_usuario_retrieve',
    summary="Dashboard Pessoal do Usuário",
    description="Retorna dados personalizados para o dashboard do usuário autenticado, incluindo projetos gerenciados, suas tarefas por status, tarefas atrasadas e próximas tarefas. Requer autenticação.",
    responses={
        200: OpenApiResponse(
            response=DashboardUsuarioSerializer,
            description="Dados consolidados para o dashboard do usuário.",
            examples=[
                OpenApiExample(
                    name="Exemplo de Dashboard do Usuário",
                    summary="Exemplo de dados retornados para o dashboard pessoal.",
                    value={
                        'projetos_gerenciados': 2,
                        'tarefas_por_status': [
                            {'status': 'Pendente', 'count': 3},
                            {'status': 'Em Andamento', 'count': 2},
                            {'status': 'Concluída', 'count': 5}
                        ],
                        'tarefas_atrasadas': 1,
                        'proximas_tarefas': [
                            {
                                'titulo': 'Implementar login',
                                'data_inicio': '2023-05-15T10:00:00Z',
                                'projeto__titulo': 'Sistema de Gestão'
                            },
                            {
                                'titulo': 'Revisar documentação API',
                                'data_inicio': '2023-05-16T09:00:00Z',
                                'projeto__titulo': 'Plataforma XPTO'
                            }
                        ]
                    }
                )
            ]
        )
    },
    tags=['Dashboard', 'Usuários']
)
@api_view(['GET'])
@extend_schema(
    summary="Dashboard do usuário",
    description="Retorna dados específicos para o dashboard do usuário logado",
    responses={
        200: DashboardUsuarioSerializer,
        401: ErrorSerializer
    }
)
def dashboard_usuario(request):
    """
    Retorna dados específicos para o dashboard do usuário.
    """
    user = request.user
    
    # Projetos onde o usuário é gerente
    projetos_gerenciados = Projeto.objects.filter(gerente=user).count()
    
    # Tarefas atribuídas ao usuário
    tarefas_usuario = Tarefa.objects.filter(responsavel=user)
    tarefas_por_status = tarefas_usuario.values('status').annotate(count=Count('id'))
    
    # Tarefas atrasadas
    tarefas_atrasadas = tarefas_usuario.filter(
        data_fim__lt=timezone.now(),
        status__in=['A_FAZER', 'EM_ANDAMENTO']
    ).count()
    
    # Próximas tarefas
    proximas_tarefas = tarefas_usuario.filter(
        data_inicio__gte=timezone.now()
    ).order_by('data_inicio')[:5].values('titulo', 'data_inicio', 'projeto__titulo')
    
    # Converter os status para nomes mais amigáveis
    status_map = {
        'A_FAZER': 'Pendente',
        'EM_ANDAMENTO': 'Em Andamento',
        'FEITO': 'Concluída',
        'BLOQUEADA': 'Bloqueada',
        'CANCELADA': 'Cancelada'
    }
    
    tarefas_por_status_formatted = [
        {'status': status_map.get(item['status'], item['status']), 'count': item['count']}
        for item in tarefas_por_status
    ]
    
    return Response({
        'projetos_gerenciados': projetos_gerenciados,
        'tarefas_por_status': tarefas_por_status_formatted,
        'tarefas_atrasadas': tarefas_atrasadas,
        'proximas_tarefas': proximas_tarefas
    })

user_dashboard = dashboard_usuario
