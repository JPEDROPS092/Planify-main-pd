from django.contrib import admin
from .models import Tarefa, AtribuicaoTarefa, ComentarioTarefa, HistoricoStatusTarefa

def get_all_fields(model):
    return [field.name for field in model._meta.fields]

class AtribuicaoTarefaInline(admin.TabularInline):
    model = AtribuicaoTarefa
    extra = 1
    autocomplete_fields = ['tarefa']

class ComentarioTarefaInline(admin.TabularInline):
    model = ComentarioTarefa
    extra = 1
    readonly_fields = ['criado_em']
    autocomplete_fields = []

class HistoricoStatusTarefaInline(admin.TabularInline):
    model = HistoricoStatusTarefa
    extra = 0
    readonly_fields = ['status_anterior', 'novo_status', 'alterado_por', 'alterado_em']
    can_delete = False
    max_num = 0
    
@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'projeto', 'sprint', 'status', 'prioridade', 'data_inicio', 'data_termino']
    list_filter = ['status', 'prioridade', 'projeto', 'sprint']
    search_fields = ['titulo', 'descricao']
    date_hierarchy = 'data_inicio'
    readonly_fields = ['criado_em', 'atualizado_em']
    autocomplete_fields = ['projeto']
    inlines = [AtribuicaoTarefaInline, ComentarioTarefaInline, HistoricoStatusTarefaInline]
    fieldsets = [
        ('Informações Básicas', {'fields': ['titulo', 'descricao', 'status', 'prioridade']}),
        ('Projeto', {'fields': ['projeto', 'sprint']}),
        ('Datas', {'fields': ['data_inicio', 'data_termino']}),
        ('Metadados', {'fields': ['criado_por', 'criado_em', 'atualizado_em']}),
    ]

@admin.register(AtribuicaoTarefa)
class AtribuicaoTarefaAdmin(admin.ModelAdmin):
    list_display = ['tarefa', 'usuario', 'atribuido_em', 'atribuido_por']
    list_filter = ['atribuido_em']
    search_fields = ['tarefa__titulo', 'usuario__username', 'usuario__email']
    date_hierarchy = 'atribuido_em'
    autocomplete_fields = ['tarefa']

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
