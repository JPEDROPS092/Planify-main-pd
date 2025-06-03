from django.contrib import admin
from .models import Projeto, MembroProjeto, HistoricoStatusProjeto, Sprint

def get_all_fields(model):
    return [field.name for field in model._meta.fields]

@admin.register(Projeto)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'status', 'prioridade', 'data_inicio', 'data_fim', 'criado_por', 'arquivado']
    list_filter = ['status', 'prioridade', 'arquivado']
    search_fields = ['titulo', 'descricao']
    date_hierarchy = 'data_inicio'
    readonly_fields = ['criado_em', 'atualizado_em']
    fieldsets = [
        ('Informações Básicas', {'fields': ['titulo', 'descricao', 'status', 'prioridade', 'arquivado']}),
        ('Datas', {'fields': ['data_inicio', 'data_fim']}),
        ('Metadados', {'fields': ['criado_por', 'criado_em', 'atualizado_em']}),
    ]

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
    list_display = ['nome', 'projeto', 'status', 'data_inicio', 'data_fim', 'criado_por']
    list_filter = ['status', 'data_inicio', 'data_fim']
    search_fields = ['nome', 'projeto__titulo', 'descricao']
    date_hierarchy = 'data_inicio'
    autocomplete_fields = ['projeto', 'criado_por']
    fieldsets = [
        ('Informações Básicas', {'fields': ['nome', 'descricao', 'projeto', 'status']}),
        ('Datas', {'fields': ['data_inicio', 'data_fim']}),
        ('Metadados', {'fields': ['criado_por']}),
    ]
