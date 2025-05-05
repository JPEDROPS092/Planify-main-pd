from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from projects.models import Projeto
from tasks.models import Tarefa
from risks.models import Risco
from costs.models import Custo
from .decorators import swagger_schema_with_examples

@api_view(['GET'])
@permission_classes([AllowAny])
def api_documentation(request):
    """
    Redireciona para a documentação da API.
    """
    return redirect('schema-swagger-ui')

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Endpoint para verificar se a API está funcionando
    """
    return Response({"status": "ok"})

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check_original(request):
    """
    Endpoint simples para verificar se a API está funcionando.
    Não requer autenticação.
    """
    return Response(
        {
            "status": "online",
            "message": "API está funcionando corretamente"
        },
        status=status.HTTP_200_OK
    )

@swagger_auto_schema(
    method='get',
    operation_description="Endpoint para obter dados do dashboard",
    responses={
        200: openapi.Response(
            description="Dados do dashboard",
            examples={
                "application/json": {
                    'total_projects': 5,
                    'total_tasks': 15,
                    'total_teams': 3,
                    'recent_activities': [
                        {'type': 'project', 'action': 'created', 'name': 'Projeto A'},
                        {'type': 'task', 'action': 'completed', 'name': 'Tarefa 1'},
                        {'type': 'team', 'action': 'updated', 'name': 'Equipe X'}
                    ]
                }
            }
        )
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_overview(request):
    """
    Endpoint para obter dados do dashboard
    """
    data = {
        'total_projects': 5,
        'total_tasks': 15,
        'total_teams': 3,
        'recent_activities': [
            {'type': 'project', 'action': 'created', 'name': 'Projeto A'},
            {'type': 'task', 'action': 'completed', 'name': 'Tarefa 1'},
            {'type': 'team', 'action': 'updated', 'name': 'Equipe X'}
        ]
    }
    return Response(data)

@swagger_auto_schema(
    method='get',
    operation_description="Retorna métricas específicas de um projeto",
    manual_parameters=[
        openapi.Parameter(
            'project_id',
            openapi.IN_PATH,
            description="ID do projeto",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Métricas do projeto",
            examples={
                "application/json": {
                    'tarefas_por_status': [
                        {'status': 'A_FAZER', 'count': 5},
                        {'status': 'EM_ANDAMENTO', 'count': 3},
                        {'status': 'FEITO', 'count': 7}
                    ],
                    'progresso': 46.67,
                    'riscos_ativos': 2,
                    'custos_totais': 15000.0,
                    'dias_restantes': 30
                }
            }
        ),
        404: openapi.Response(
            description="Projeto não encontrado",
            examples={
                "application/json": {
                    "error": "Projeto não encontrado"
                }
            }
        )
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def project_metrics(request, project_id):
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
    
    return Response({
        'tarefas_por_status': tarefas_por_status,
        'progresso': progresso,
        'riscos_ativos': riscos_ativos,
        'custos_totais': custos_totais['total'] or 0,
        'dias_restantes': dias_restantes
    })

@swagger_auto_schema(
    method='get',
    operation_description="Retorna dados específicos para o dashboard do usuário",
    responses={
        200: openapi.Response(
            description="Dados do dashboard do usuário",
            examples={
                "application/json": {
                    'projetos_gerenciados': 2,
                    'tarefas_por_status': [
                        {'status': 'A_FAZER', 'count': 3},
                        {'status': 'EM_ANDAMENTO', 'count': 2},
                        {'status': 'FEITO', 'count': 5}
                    ],
                    'tarefas_atrasadas': 1,
                    'proximas_tarefas': [
                        {
                            'titulo': 'Implementar login',
                            'data_inicio': '2023-05-15T10:00:00Z',
                            'projeto__titulo': 'Sistema de Gestão'
                        }
                    ]
                }
            }
        )
    }
)
@api_view(['GET'])
def user_dashboard(request):
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
    
    return Response({
        'projetos_gerenciados': projetos_gerenciados,
        'tarefas_por_status': tarefas_por_status,
        'tarefas_atrasadas': tarefas_atrasadas,
        'proximas_tarefas': proximas_tarefas
    })
