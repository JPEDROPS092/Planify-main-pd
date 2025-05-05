from django.contrib import admin
from .models import Projeto, MembroProjeto, HistoricoStatusProjeto, Sprint

def get_all_fields(model):
    return [field.name for field in model._meta.fields]

@admin.register(Projeto)
class ProjectAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Projeto)
    list_filter = get_all_fields(Projeto)
    search_fields = ['name', 'description']

@admin.register(MembroProjeto)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = get_all_fields(MembroProjeto)
    list_filter = get_all_fields(MembroProjeto)
    search_fields = ['project__name', 'user__username']

@admin.register(HistoricoStatusProjeto)
class ProjectStatusHistoryAdmin(admin.ModelAdmin):
    list_display = get_all_fields(HistoricoStatusProjeto)
    list_filter = get_all_fields(HistoricoStatusProjeto)
    search_fields = ['project__name', 'previous_status', 'new_status']

@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Sprint)
    list_filter = get_all_fields(Sprint)
    search_fields = ['project__name', 'name']
