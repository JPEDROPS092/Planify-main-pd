from django.contrib import admin
from .models import Categoria, Custo, OrcamentoProjeto, OrcamentoTarefa, Alerta

def get_all_fields(model):
    return [field.name for field in model._meta.fields]

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = tuple(get_all_fields(Categoria))
    list_filter = tuple(get_all_fields(Categoria))
    search_fields = ['nome', 'descricao']

@admin.register(Custo)
class CustoAdmin(admin.ModelAdmin):
    list_display = tuple(get_all_fields(Custo))
    list_filter = tuple(get_all_fields(Custo))
    search_fields = ['descricao', 'projeto__name', 'tarefa__titulo']

@admin.register(OrcamentoProjeto)
class OrcamentoProjetoAdmin(admin.ModelAdmin):
    list_display = tuple(get_all_fields(OrcamentoProjeto))
    list_filter = tuple(get_all_fields(OrcamentoProjeto))
    search_fields = ['projeto__name']

@admin.register(OrcamentoTarefa)
class OrcamentoTarefaAdmin(admin.ModelAdmin):
    list_display = tuple(get_all_fields(OrcamentoTarefa))
    list_filter = tuple(get_all_fields(OrcamentoTarefa))
    search_fields = ['tarefa__titulo']

@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = tuple(get_all_fields(Alerta))
    list_filter = tuple(get_all_fields(Alerta))
    search_fields = ['projeto__name', 'tarefa__titulo', 'mensagem', 'status']
