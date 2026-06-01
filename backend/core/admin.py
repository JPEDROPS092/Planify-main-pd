from django.contrib import admin
from django.db.models import Count

from projects.models import Projeto, Sprint
from tasks.models import Tarefa
from users.models import User

admin.site.site_header = 'Planify - Administração'
admin.site.site_title = 'Planify - Sistema de Gerenciamento de Projetos'
admin.site.index_title = 'Dashboard'

def get_admin_index(self, request, extra_context=None):
    """Custom admin dashboard with key metrics and charts"""
    extra_context = extra_context or {}

    total_projetos = Projeto.objects.count()
    projetos_ativos = Projeto.objects.filter(arquivado=False).count()
    total_tarefas = Tarefa.objects.count()
    tarefas_concluidas = Tarefa.objects.filter(status='concluida').count()
    total_usuarios = User.objects.count()

    projetos_por_status = Projeto.objects.values('status').annotate(
        total=Count('id')
    ).order_by('status')

    tarefas_por_status = Tarefa.objects.values('status').annotate(
        total=Count('id')
    ).order_by('status')

    projetos_recentes = Projeto.objects.order_by('-criado_em')[:5]
    tarefas_recentes = Tarefa.objects.order_by('-criado_em')[:5]

    extra_context.update({
        'total_projetos': total_projetos,
        'projetos_ativos': projetos_ativos,
        'total_tarefas': total_tarefas,
        'tarefas_concluidas': tarefas_concluidas,
        'total_usuarios': total_usuarios,
        'projetos_por_status': projetos_por_status,
        'tarefas_por_status': tarefas_por_status,
        'projetos_recentes': projetos_recentes,
        'tarefas_recentes': tarefas_recentes,
    })

    return admin.site.__class__.index(self, request, extra_context)

admin.site.index = get_admin_index.__get__(admin.site)
