from django.contrib import admin
from .models import Documento, HistoricoDocumento, Comentario

def get_all_fields(model):
    return [field.name for field in model._meta.fields]

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Documento)
    list_filter = get_all_fields(Documento)
    search_fields = ['titulo', 'descricao', 'projeto__name', 'tarefa__titulo']

@admin.register(HistoricoDocumento)
class HistoricoDocumentoAdmin(admin.ModelAdmin):
    list_display = get_all_fields(HistoricoDocumento)
    list_filter = get_all_fields(HistoricoDocumento)
    search_fields = ['documento__titulo', 'versao_anterior']

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Comentario)
    list_filter = get_all_fields(Comentario)
    search_fields = ['documento__titulo', 'autor__username', 'texto']
