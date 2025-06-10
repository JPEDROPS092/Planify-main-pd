from django.contrib import admin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.db.models import Count, Sum
from django.contrib.admin.models import LogEntry

# Import models from various apps
from projects.models import Projeto, Sprint, MembroProjeto, HistoricoStatusProjeto
from tasks.models import Tarefa, AtribuicaoTarefa, ComentarioTarefa, HistoricoStatusTarefa
from users.models import User
from risks.models import Risco
from costs.models import Custo
from documents.models import Documento
from communications.models import Notificacao

# Register models from various apps with default admin
class CustomAdmin(admin.ModelAdmin):
    """Base admin class with common functionality"""
    list_per_page = 25
    date_hierarchy = 'criado_em'
    empty_value_display = '---'
    
    def get_fieldsets(self, request, obj=None):
        """Add common fieldsets to all admin models"""
        fieldsets = super().get_fieldsets(request, obj)
        return fieldsets

# Customize admin site
admin.site.site_header = 'Planify - Administração'
admin.site.site_title = 'Planify - Sistema de Gerenciamento de Projetos'
admin.site.index_title = 'Dashboard'

# Project admin customizations
class MembroProjetoInline(admin.TabularInline):
    model = MembroProjeto
    extra = 1
    autocomplete_fields = ['usuario']

class SprintInline(admin.TabularInline):
    model = Sprint
    extra = 0
    fields = ['nome', 'status', 'data_inicio', 'data_fim']
    show_change_link = True

@admin.register(Projeto)
class ProjetoAdmin(CustomAdmin):
    list_display = ['titulo', 'status', 'prioridade', 'data_inicio', 'data_fim', 'criado_por', 'get_membros_count', 'get_tarefas_count']
    list_filter = ['status', 'prioridade', 'arquivado']
    search_fields = ['titulo', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em', 'get_membros_count', 'get_tarefas_count']
    inlines = [MembroProjetoInline, SprintInline]
    
    fieldsets = [
        ('Informações Básicas', {'fields': ['titulo', 'descricao', 'status', 'prioridade', 'arquivado']}),
        ('Datas', {'fields': ['data_inicio', 'data_fim']}),
        ('Metadados', {'fields': ['criado_por', 'criado_em', 'atualizado_em']}),
        ('Estatísticas', {'fields': ['get_membros_count', 'get_tarefas_count'], 'classes': ['collapse']}),
    ]
    
    def get_membros_count(self, obj):
        return obj.membros.count()
    get_membros_count.short_description = 'Total de Membros'
    
    def get_tarefas_count(self, obj):
        return obj.tarefas.count()
    get_tarefas_count.short_description = 'Total de Tarefas'

@admin.register(Sprint)
class SprintAdmin(CustomAdmin):
    list_display = ['nome', 'projeto', 'status', 'data_inicio', 'data_fim', 'get_tarefas_count']
    list_filter = ['status', 'data_inicio', 'data_fim']
    search_fields = ['nome', 'projeto__titulo', 'descricao']
    autocomplete_fields = ['projeto', 'criado_por']
    
    def get_tarefas_count(self, obj):
        return obj.tarefas.count()
    get_tarefas_count.short_description = 'Total de Tarefas'

# Task admin customizations
class AtribuicaoTarefaInline(admin.TabularInline):
    model = AtribuicaoTarefa
    extra = 1

class ComentarioTarefaInline(admin.TabularInline):
    model = ComentarioTarefa
    extra = 0
    readonly_fields = ['criado_em']

@admin.register(Tarefa)
class TarefaAdmin(CustomAdmin):
    list_display = ['titulo', 'projeto', 'sprint', 'status', 'prioridade', 'data_inicio', 'data_termino', 'get_responsaveis']
    list_filter = ['status', 'prioridade', 'projeto', 'sprint']
    search_fields = ['titulo', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em']
    inlines = [AtribuicaoTarefaInline, ComentarioTarefaInline]
    
    def get_responsaveis(self, obj):
        responsaveis = obj.atribuicoes.all()[:3]
        if not responsaveis:
            return '---'
        return ', '.join([a.usuario.username for a in responsaveis])
    get_responsaveis.short_description = 'Responsáveis'

# Custom admin dashboard
def get_admin_index(self, request, extra_context=None):
    """Custom admin dashboard with key metrics and charts"""
    extra_context = extra_context or {}
    
    # Dashboard metrics
    total_projetos = Projeto.objects.count()
    projetos_ativos = Projeto.objects.filter(arquivado=False).count()
    total_tarefas = Tarefa.objects.count()
    tarefas_concluidas = Tarefa.objects.filter(status='concluida').count()
    total_usuarios = User.objects.count()
    
    # Projects by status
    projetos_por_status = Projeto.objects.values('status').annotate(
        total=Count('id')
    ).order_by('status')
    
    # Tasks by status
    tarefas_por_status = Tarefa.objects.values('status').annotate(
        total=Count('id')
    ).order_by('status')
    
    # Recent projects
    projetos_recentes = Projeto.objects.order_by('-criado_em')[:5]
    
    # Recent tasks
    tarefas_recentes = Tarefa.objects.order_by('-criado_em')[:5]
    
    # Add all context data
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

# Set the custom dashboard as the index view
admin.site.index = get_admin_index.__get__(admin.site)