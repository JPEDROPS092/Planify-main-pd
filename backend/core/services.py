"""
Camada de serviços do módulo core.

Este módulo fornece serviços centralizados que podem ser reutilizados
por diferentes partes da aplicação. Ele implementa a lógica de negócio
que é comum a múltiplos componentes ou que integra vários subsistemas.
"""

from django.db.models import Count, Sum, Q
from django.utils import timezone

from projects.models import Projeto
from tasks.models import Tarefa
from risks.models import Risco
from costs.models import Custo

# Mapeamento de status técnicos para nomes amigáveis ao usuário
STATUS_AMIGAVEL = {
    'A_FAZER': 'Pendente',
    'EM_ANDAMENTO': 'Em Andamento',
    'FEITO': 'Concluída',
    'BLOQUEADA': 'Bloqueada',
    'CANCELADA': 'Cancelada'
}

def obter_status_formatado(status_tecnico):
    """
    Converte um código de status técnico para um nome amigável ao usuário.
    
    Args:
        status_tecnico (str): Código interno do status (ex: 'A_FAZER')
        
    Returns:
        str: Nome formatado do status (ex: 'Pendente')
    """
    return STATUS_AMIGAVEL.get(status_tecnico, status_tecnico)

def formatar_contagem_tarefas_por_status(tarefas_por_status):
    """
    Formata a contagem de tarefas por status para exibição amigável.
    
    Args:
        tarefas_por_status (QuerySet): Resultado de uma query com values('status') e annotate(count=Count('id'))
        
    Returns:
        list: Lista formatada com status amigáveis e contagens
    """
    return [
        {'status': obter_status_formatado(item['status']), 'count': item['count']}
        for item in tarefas_por_status
    ]

def calcular_metricas_projeto(projeto_id):
    """
    Calcula métricas detalhadas para um projeto específico.
    
    Args:
        projeto_id (int): ID do projeto
        
    Returns:
        dict: Dicionário com métricas do projeto ou None se o projeto não existir
        
    Raises:
        Projeto.DoesNotExist: Se o projeto não for encontrado
    """
    projeto = Projeto.objects.get(id=projeto_id)
    
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
    
    # Converter os status para nomes amigáveis
    tarefas_por_status_formatado = formatar_contagem_tarefas_por_status(tarefas_por_status)
    
    return {
        'tarefas_por_status': tarefas_por_status_formatado,
        'progresso': progresso,
        'riscos_ativos': riscos_ativos,
        'custos_totais': custos_totais['total'] or 0,
        'dias_restantes': dias_restantes
    }

def obter_metricas_usuario(usuario):
    """
    Obtém métricas personalizadas para o dashboard do usuário.
    
    Args:
        usuario (User): Objeto do usuário autenticado
        
    Returns:
        dict: Dicionário com métricas do usuário
    """
    # Projetos onde o usuário é gerente
    projetos_gerenciados = Projeto.objects.filter(gerente=usuario).count()
    
    # Tarefas atribuídas ao usuário
    tarefas_usuario = Tarefa.objects.filter(responsavel=usuario)
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
    
    # Converter os status para nomes amigáveis
    tarefas_por_status_formatado = formatar_contagem_tarefas_por_status(tarefas_por_status)
    
    return {
        'projetos_gerenciados': projetos_gerenciados,
        'tarefas_por_status': tarefas_por_status_formatado,
        'tarefas_atrasadas': tarefas_atrasadas,
        'proximas_tarefas': proximas_tarefas
    }
