from django.contrib import admin
from .models import Risco, HistoricoRisco

def get_all_fields(model):
    return [field.name for field in model._meta.fields]

@admin.register(Risco)
class RiscoAdmin(admin.ModelAdmin):
    list_display = tuple(get_all_fields(Risco))
    list_filter = tuple(get_all_fields(Risco))
    search_fields = ['descricao', 'projeto__name', 'status', 'probabilidade', 'impacto']

@admin.register(HistoricoRisco)
class HistoricoRiscoAdmin(admin.ModelAdmin):
    list_display = tuple(get_all_fields(HistoricoRisco))
    list_filter = tuple(get_all_fields(HistoricoRisco))
    search_fields = ['risco__descricao', 'status_anterior', 'novo_status']
