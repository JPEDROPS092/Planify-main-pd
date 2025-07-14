from django.contrib import admin
from .models import Tarefa, AtribuicaoTarefa, ComentarioTarefa, HistoricoStatusTarefa

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'projeto', 'status', 'prioridade', 'criado_por', 'data_termino']
    list_filter = ['status', 'prioridade', 'data_termino', 'criado_em']
    search_fields = ['titulo', 'descricao', 'projeto__titulo', 'criado_por__username']
    date_hierarchy = 'criado_em'
    readonly_fields = ['criado_em', 'atualizado_em']
    autocomplete_fields = ['projeto', 'criado_por', 'sprint']

# Registros simples sem customização
admin.site.register(AtribuicaoTarefa)

@admin.register(ComentarioTarefa)
class ComentarioTarefaAdmin(admin.ModelAdmin):
    list_display = ['tarefa', 'autor', 'texto_resumido', 'criado_em']
    list_filter = ['criado_em']
    search_fields = ['tarefa__titulo', 'autor__username', 'texto']
    date_hierarchy = 'criado_em'
    readonly_fields = ['criado_em']
    autocomplete_fields = ['tarefa']
    
    def texto_resumido(self, obj):
        return obj.texto[:50] + '...' if len(obj.texto) > 50 else obj.texto
    texto_resumido.short_description = 'Texto'

@admin.register(HistoricoStatusTarefa)
class HistoricoStatusTarefaAdmin(admin.ModelAdmin):
    list_display = ['tarefa', 'status_anterior', 'novo_status', 'alterado_por', 'alterado_em']
    list_filter = ['status_anterior', 'novo_status', 'alterado_em']
    search_fields = ['tarefa__titulo']
    date_hierarchy = 'alterado_em'
    readonly_fields = ['alterado_em']
    autocomplete_fields = ['tarefa']
