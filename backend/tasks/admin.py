from django.contrib import admin
from .models import Tarefa, AtribuicaoTarefa, ComentarioTarefa, HistoricoStatusTarefa

def get_all_fields(model):
    return [field.name for field in model._meta.fields]

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Tarefa)
    list_filter = get_all_fields(Tarefa)
    search_fields = ['titulo', 'descricao']

@admin.register(AtribuicaoTarefa)
class AtribuicaoTarefaAdmin(admin.ModelAdmin):
    list_display = get_all_fields(AtribuicaoTarefa)
    list_filter = get_all_fields(AtribuicaoTarefa)
    search_fields = ['tarefa__titulo', 'usuario__username']

@admin.register(ComentarioTarefa)
class ComentarioTarefaAdmin(admin.ModelAdmin):
    list_display = get_all_fields(ComentarioTarefa)
    list_filter = get_all_fields(ComentarioTarefa)
    search_fields = ['tarefa__titulo', 'autor__username', 'texto']

@admin.register(HistoricoStatusTarefa)
class HistoricoStatusTarefaAdmin(admin.ModelAdmin):
    list_display = get_all_fields(HistoricoStatusTarefa)
    list_filter = get_all_fields(HistoricoStatusTarefa)
    search_fields = ['tarefa__titulo', 'status_anterior', 'novo_status']
