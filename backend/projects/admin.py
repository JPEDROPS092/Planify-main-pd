from django.contrib import admin
from .models import Projeto, MembroProjeto, HistoricoStatusProjeto, Sprint

@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'status', 'criado_por', 'data_inicio', 'data_fim']
    list_filter = ['status', 'data_inicio', 'data_fim']
    search_fields = ['titulo', 'descricao', 'criado_por__username']
    date_hierarchy = 'data_inicio'
    readonly_fields = ['criado_em', 'atualizado_em']
    autocomplete_fields = ['criado_por']

@admin.register(MembroProjeto)
class MembroProjetoAdmin(admin.ModelAdmin):
    list_display = ['projeto', 'usuario', 'papel']
    list_filter = ['papel']
    search_fields = ['projeto__titulo', 'usuario__username', 'usuario__email']
    autocomplete_fields = ['projeto', 'usuario']

@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ['nome', 'projeto', 'status', 'data_inicio', 'data_fim']
    list_filter = ['status', 'data_inicio', 'data_fim']
    search_fields = ['nome', 'descricao', 'projeto__titulo']
    date_hierarchy = 'data_inicio'
    readonly_fields = ['criado_em']
    autocomplete_fields = ['projeto', 'criado_por']

# Registros simples sem customização
admin.site.register(HistoricoStatusProjeto)
