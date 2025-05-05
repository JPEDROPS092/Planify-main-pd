from django.contrib import admin
from .models import Equipe, MembroEquipe, PermissaoEquipe

def get_all_fields(model):
    return [field.name for field in model._meta.fields]

class MembroEquipeInline(admin.TabularInline):
    model = MembroEquipe
    extra = 1
    autocomplete_fields = ['usuario', 'adicionado_por']

class PermissaoEquipeInline(admin.TabularInline):
    model = PermissaoEquipe
    extra = 1

@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'criado_por', 'criado_em']
    list_filter = ['criado_em']
    search_fields = ['nome', 'descricao']
    date_hierarchy = 'criado_em'
    readonly_fields = ['criado_em', 'atualizado_em']
    autocomplete_fields = ['criado_por']
    inlines = [MembroEquipeInline, PermissaoEquipeInline]
    fieldsets = [
        ('Informações Básicas', {'fields': ['nome', 'descricao']}),
        ('Metadados', {'fields': ['criado_por', 'criado_em', 'atualizado_em']}),
    ]

@admin.register(MembroEquipe)
class MembroEquipeAdmin(admin.ModelAdmin):
    list_display = ['equipe', 'usuario', 'papel', 'adicionado_em', 'adicionado_por']
    list_filter = ['papel', 'adicionado_em']
    search_fields = ['equipe__nome', 'usuario__username', 'usuario__email']
    date_hierarchy = 'adicionado_em'
    autocomplete_fields = ['equipe', 'usuario', 'adicionado_por']

@admin.register(PermissaoEquipe)
class PermissaoEquipeAdmin(admin.ModelAdmin):
    list_display = ['equipe', 'papel', 'modulo', 'permissao']
    list_filter = ['papel', 'modulo', 'permissao']
    search_fields = ['equipe__nome']
    autocomplete_fields = ['equipe']
