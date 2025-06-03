from django.db import models
from django.conf import settings
from projects.models import Projeto
from tasks.models import Tarefa

class ChatMensagem(models.Model):
    """Modelo para mensagens de chat em projetos"""
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='mensagens')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    texto = models.TextField()
    anexo = models.FileField(upload_to='chat_anexos/', blank=True, null=True)
    enviado_em = models.DateTimeField(auto_now_add=True)
    editado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Mensagem de {self.autor.username} em {self.projeto.titulo}"
    
    class Meta:
        verbose_name = 'Mensagem de Chat'
        verbose_name_plural = 'Mensagens de Chat'
        ordering = ['enviado_em']


class ChatMensagemLeitura(models.Model):
    """Registro de leitura de mensagens por usuários"""
    mensagem = models.ForeignKey(ChatMensagem, on_delete=models.CASCADE, related_name='leituras')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensagens_lidas')
    lido_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Mensagem de {self.mensagem.autor.username} em {self.mensagem.projeto.titulo} lida por {self.usuario.username}"
    
    class Meta:
        unique_together = ('mensagem', 'usuario')
        verbose_name = 'Leitura de Mensagem'
        verbose_name_plural = 'Leituras de Mensagens'


class Notificacao(models.Model):
    """Modelo para notificações do sistema"""
    TIPO_CHOICES = (
        ('TAREFA', 'Tarefa'),
        ('PROJETO', 'Projeto'),
        ('EQUIPE', 'Equipe'),
        ('RISCO', 'Risco'),
        ('DOCUMENTO', 'Documento'),
        ('SISTEMA', 'Sistema'),
    )
    
    PRIORIDADE_CHOICES = (
        ('BAIXA', 'Baixa'),
        ('MEDIA', 'Média'),
        ('ALTA', 'Alta'),
    )
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificacoes')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default='MEDIA')
    criada_em = models.DateTimeField(auto_now_add=True)
    lida_em = models.DateTimeField(null=True, blank=True)
    
    # Referências opcionais para objetos relacionados
    projeto = models.ForeignKey(Projeto, on_delete=models.SET_NULL, null=True, blank=True)
    tarefa = models.ForeignKey(Tarefa, on_delete=models.SET_NULL, null=True, blank=True)
    url = models.CharField(max_length=255, blank=True, null=True, help_text='URL para redirecionamento')
    
    def __str__(self):
        return f"{self.get_tipo_display()}: {self.titulo} para {self.usuario.username}"
    
    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-criada_em']


class ConfiguracaoNotificacao(models.Model):
    """Configurações de notificações por usuário"""
    CANAL_CHOICES = (
        ('EMAIL', 'E-mail'),
        ('SISTEMA', 'Sistema'),
        ('AMBOS', 'Ambos'),
        ('NENHUM', 'Nenhum'),
    )
    
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='config_notificacoes')
    
    # Configurações por tipo de evento
    tarefa_atribuida = models.CharField(max_length=10, choices=CANAL_CHOICES, default='AMBOS')
    tarefa_comentario = models.CharField(max_length=10, choices=CANAL_CHOICES, default='SISTEMA')
    tarefa_prazo = models.CharField(max_length=10, choices=CANAL_CHOICES, default='AMBOS')
    projeto_status = models.CharField(max_length=10, choices=CANAL_CHOICES, default='SISTEMA')
    equipe_alteracao = models.CharField(max_length=10, choices=CANAL_CHOICES, default='SISTEMA')
    documento_novo = models.CharField(max_length=10, choices=CANAL_CHOICES, default='SISTEMA')
    risco_novo = models.CharField(max_length=10, choices=CANAL_CHOICES, default='SISTEMA')
    mensagem_chat = models.CharField(max_length=10, choices=CANAL_CHOICES, default='SISTEMA')
    
    def __str__(self):
        return f"Configurações de notificação para {self.usuario.username}"
    
    class Meta:
        verbose_name = 'Configuração de Notificação'
        verbose_name_plural = 'Configurações de Notificações'


class Comunicacao(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='comunicacoes')
    titulo = models.CharField(max_length=200)
    texto = models.TextField()
    remetente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comunicacoes_enviadas')
    destinatarios = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comunicacoes_recebidas')
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-criada_em']
        verbose_name = 'Comunicação'
        verbose_name_plural = 'Comunicações'
    
    def __str__(self):
        return self.titulo
