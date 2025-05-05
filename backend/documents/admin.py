from django.contrib import admin
from .models import Documento, HistoricoDocumento, Comentario

def get_all_fields(model):
    return [field.name for field in model._meta.fields]

class HistoricoDocumentoInline(admin.TabularInline):
    model = HistoricoDocumento
    extra = 0
    readonly_fields = ['versao_anterior', 'alterado_por', 'data_alteracao']
    can_delete = False
    max_num = 0

class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 1
    readonly_fields = ['criado_em']
    autocomplete_fields = ['autor']

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'projeto', 'tipo', 'versao', 'enviado_por', 'data_upload']
    list_filter = ['tipo', 'data_upload', 'projeto']
    search_fields = ['titulo', 'descricao', 'projeto__titulo', 'tarefa__titulo']
    date_hierarchy = 'data_upload'
    readonly_fields = ['data_upload', 'atualizado_em', 'tamanho_arquivo', 'tipo_arquivo']
    autocomplete_fields = ['projeto', 'tarefa', 'enviado_por']
    inlines = [HistoricoDocumentoInline, ComentarioInline]
    fieldsets = [
        ('Informações Básicas', {'fields': ['titulo', 'descricao', 'tipo', 'versao']}),
        ('Arquivo', {'fields': ['arquivo', 'tamanho_arquivo', 'tipo_arquivo']}),
        ('Relacionamentos', {'fields': ['projeto', 'tarefa']}),
        ('Metadados', {'fields': ['enviado_por', 'data_upload', 'atualizado_em']}),
    ]

@admin.register(HistoricoDocumento)
class HistoricoDocumentoAdmin(admin.ModelAdmin):
    list_display = ['documento', 'versao_anterior', 'alterado_por', 'data_alteracao']
    list_filter = ['data_alteracao']
    search_fields = ['documento__titulo']
    date_hierarchy = 'data_alteracao'
    readonly_fields = ['data_alteracao']
    autocomplete_fields = ['documento', 'alterado_por']

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['documento', 'autor', 'texto_resumido', 'criado_em']
    list_filter = ['criado_em']
    search_fields = ['documento__titulo', 'autor__username', 'texto']
    date_hierarchy = 'criado_em'
    readonly_fields = ['criado_em']
    autocomplete_fields = ['documento', 'autor']
    
    def texto_resumido(self, obj):
        return obj.texto[:50] + '...' if len(obj.texto) > 50 else obj.texto
    texto_resumido.short_description = 'Texto'
