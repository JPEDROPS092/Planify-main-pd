from django.contrib import admin
from .models import ChatMensagem, ChatMensagemLeitura, Notificacao, ConfiguracaoNotificacao, Comunicacao

@admin.register(ChatMensagem)
class ChatMensagemAdmin(admin.ModelAdmin):
    list_display = ['id', 'projeto', 'autor', 'enviado_em', 'editado']
    list_filter = ['projeto', 'autor', 'enviado_em', 'editado']
    search_fields = ['projeto__titulo', 'autor__username', 'texto']
    date_hierarchy = 'enviado_em'

@admin.register(ChatMensagemLeitura)
class ChatMensagemLeituraAdmin(admin.ModelAdmin):
    list_display = ['id', 'mensagem', 'usuario', 'lido_em']
    list_filter = ['usuario', 'lido_em']
    search_fields = ['mensagem__texto', 'usuario__username']
    date_hierarchy = 'lido_em'

@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'tipo', 'titulo', 'lida', 'criada_em']
    list_filter = ['tipo', 'lida', 'prioridade', 'criada_em']
    search_fields = ['usuario__username', 'titulo', 'mensagem']
    date_hierarchy = 'criada_em'

@admin.register(ConfiguracaoNotificacao)
class ConfiguracaoNotificacaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario']
    list_filter = ['tarefa_atribuida', 'tarefa_prazo', 'projeto_status']
    search_fields = ['usuario__username']

@admin.register(Comunicacao)
class ComunicacaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'projeto', 'tipo', 'titulo', 'remetente', 'criada_em']
    list_filter = ['tipo', 'projeto', 'criada_em']
    search_fields = ['titulo', 'texto', 'remetente__username']
    date_hierarchy = 'criada_em'
    filter_horizontal = ['destinatarios']
