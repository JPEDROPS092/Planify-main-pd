from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from projects.models import Projeto
from tasks.models import Tarefa
from risks.models import Risco
from costs.models import Custo
from .decorators import swagger_schema_with_examples

@api_view(['GET'])
@permission_classes([AllowAny])
def documentacao_api(request):
    """
    Redireciona para a documentação da API.
    """
    return redirect('openapi-schema')

@api_view(['GET'])
@permission_classes([AllowAny])
def checagem_saude(request):
    """
    Endpoint para verificar se a API está funcionando
    """
    return Response({"status": "ok"})

@api_view(['GET'])
@permission_classes([AllowAny])
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

@swagger_schema_with_examples(
    method='get',
    operation_description="Endpoint para obter dados do dashboard",
    responses={
        200: {
            'description': "Dados do dashboard",
            'examples': {
                "application/json": {
                    'total_projetos': 5,
                    'total_tarefas': 15,
                    'tarefas_por_status': [
                        {'status': 'Pendente', 'count': 5},
                        {'status': 'Em Andamento', 'count': 7},
                        {'status': 'Concluída', 'count': 3}
                    ]
                }
            }
        }
    }
)
@api_view(['GET'])
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

@swagger_schema_with_examples(
    method='get',
    operation_description="Retorna métricas específicas de um projeto",
    manual_parameters=[
        {
            'name': 'project_id',
            'in': 'path',
            'description': "ID do projeto",
            'type': 'integer',
            'required': True
        }
    ],
    responses={
        200: {
            'description': "Métricas do projeto",
            'examples': {
                "application/json": {
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
            }
        },
        404: {
            'description': "Projeto não encontrado",
            'examples': {
                "application/json": {
                    "error": "Projeto não encontrado"
                }
            }
        }
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
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

@swagger_schema_with_examples(
    method='get',
    operation_description="Retorna dados específicos para o dashboard do usuário",
    responses={
        200: {
            'description': "Dados do dashboard do usuário",
            'examples': {
                "application/json": {
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
                        }
                    ]
                }
            }
        }
    }
)
@api_view(['GET'])
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
