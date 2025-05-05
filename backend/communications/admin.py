from django.contrib import admin
from .models import ChatMensagem, ChatMensagemLeitura, Notificacao, ConfiguracaoNotificacao

def get_all_fields(model):
    return [field.name for field in model._meta.fields]

@admin.register(ChatMensagem)
class ChatMensagemAdmin(admin.ModelAdmin):
    list_display = get_all_fields(ChatMensagem)
    list_filter = get_all_fields(ChatMensagem)
    search_fields = ['projeto__name', 'autor__username', 'texto']

@admin.register(ChatMensagemLeitura)
class ChatMensagemLeituraAdmin(admin.ModelAdmin):
    list_display = get_all_fields(ChatMensagemLeitura)
    list_filter = get_all_fields(ChatMensagemLeitura)
    search_fields = ['mensagem__texto', 'usuario__username']

@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Notificacao)
    list_filter = get_all_fields(Notificacao)
    search_fields = ['usuario__username', 'titulo', 'mensagem', 'tipo']

@admin.register(ConfiguracaoNotificacao)
class ConfiguracaoNotificacaoAdmin(admin.ModelAdmin):
    list_display = get_all_fields(ConfiguracaoNotificacao)
    list_filter = get_all_fields(ConfiguracaoNotificacao)
    search_fields = ['usuario__username']
