from django.contrib import admin
from .models import Equipe, MembroEquipe, PermissaoEquipe

def get_all_fields(model):
    return [field.name for field in model._meta.fields]

@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Equipe)
    list_filter = get_all_fields(Equipe)
    search_fields = ['nome', 'descricao']

@admin.register(MembroEquipe)
class MembroEquipeAdmin(admin.ModelAdmin):
    list_display = get_all_fields(MembroEquipe)
    list_filter = get_all_fields(MembroEquipe)
    search_fields = ['equipe__nome', 'usuario__username', 'papel']

@admin.register(PermissaoEquipe)
class PermissaoEquipeAdmin(admin.ModelAdmin):
    list_display = get_all_fields(PermissaoEquipe)
    list_filter = get_all_fields(PermissaoEquipe)
    search_fields = ['equipe__nome', 'papel', 'modulo', 'permissao']
