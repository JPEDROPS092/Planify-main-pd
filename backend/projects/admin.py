from django.contrib import admin
from .models import Projeto, MembroProjeto, HistoricoStatusProjeto, Sprint

def get_all_fields(model):
    return [field.name for field in model._meta.fields]

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
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'status', 'prioridade', 'data_inicio', 'data_fim', 'criado_por', 'get_membros_count', 'get_tarefas_count']
    list_filter = ['status', 'prioridade', 'arquivado']
    search_fields = ['titulo', 'descricao']
    date_hierarchy = 'data_inicio'
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

@admin.register(MembroProjeto)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ['projeto', 'usuario', 'papel']  # Removed 'data_entrada'
    list_filter = ['papel']  # Removed 'data_entrada'
    search_fields = ['projeto__titulo', 'usuario__username', 'usuario__email']
    autocomplete_fields = ['projeto', 'usuario']

@admin.register(HistoricoStatusProjeto)
class ProjectStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['projeto', 'status_anterior', 'alterado_por', 'alterado_em']  # Removed 'novo_status'
    list_filter = ['status_anterior', 'alterado_em']  # Removed 'novo_status'
    search_fields = ['projeto__titulo']
    readonly_fields = ['alterado_em']
    autocomplete_fields = ['projeto', 'alterado_por']

@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ['nome', 'projeto', 'status', 'data_inicio', 'data_fim', 'get_tarefas_count']
    list_filter = ['status', 'data_inicio', 'data_fim']
    search_fields = ['nome', 'projeto__titulo', 'descricao']
    date_hierarchy = 'data_inicio'
    autocomplete_fields = ['projeto', 'criado_por']
    fieldsets = [
        ('Informações Básicas', {'fields': ['nome', 'descricao', 'projeto', 'status']}),
        ('Datas', {'fields': ['data_inicio', 'data_fim']}),
        ('Metadados', {'fields': ['criado_por']}),
    ]

    def get_tarefas_count(self, obj):
        return obj.tarefas.count()
    get_tarefas_count.short_description = 'Total de Tarefas'
