from django.db import models
from django.conf import settings
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from projects.models import Projeto
from tasks.models import Tarefa

class ChatMensagem(models.Model):
    """
    Modelo para mensagens de chat em projetos.
    
    Representa uma mensagem enviada por um usuário em um projeto específico.
    Pode conter texto e anexos opcionais. Registra quando a mensagem foi enviada
    e se foi editada posteriormente.
    """
    projeto = models.ForeignKey(
        Projeto, 
        on_delete=models.CASCADE, 
        related_name='mensagens',
        help_text='Projeto ao qual a mensagem pertence'
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='mensagens_enviadas',
        help_text='Usuário que enviou a mensagem'
    )
    texto = models.TextField(help_text='Conteúdo da mensagem')
    anexo = models.FileField(
        upload_to='chat_anexos/', 
        blank=True, 
        null=True,
        help_text='Arquivo opcional anexado à mensagem'
    )
    enviado_em = models.DateTimeField(
        auto_now_add=True,
        help_text='Data e hora em que a mensagem foi enviada'
    )
    editado = models.BooleanField(
        default=False,
        help_text='Indica se a mensagem foi editada após o envio inicial'
    )
    
    def __str__(self):
        return f"Mensagem de {self.autor.username} em {self.projeto.titulo}"
    
    class Meta:
        verbose_name = 'Mensagem de Chat'
        verbose_name_plural = 'Mensagens de Chat'
        ordering = ['enviado_em']


class ChatMensagemLeitura(models.Model):
    """
    Registro de leitura de mensagens por usuários.
    
    Rastreia quando um usuário específico leu uma determinada mensagem.
    Cada combinação de mensagem e usuário deve ser única (garantido por Meta.unique_together).
    """
    mensagem = models.ForeignKey(
        ChatMensagem, 
        on_delete=models.CASCADE, 
        related_name='leituras',
        help_text='Mensagem que foi lida'
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='mensagens_lidas',
        help_text='Usuário que leu a mensagem'
    )
    lido_em = models.DateTimeField(
        auto_now_add=True,
        help_text='Data e hora em que a mensagem foi lida'
    )
    
    def __str__(self):
        return f"Mensagem de {self.mensagem.autor.username} em {self.mensagem.projeto.titulo} lida por {self.usuario.username}"
    
    class Meta:
        unique_together = ('mensagem', 'usuario')
        verbose_name = 'Leitura de Mensagem'
        verbose_name_plural = 'Leituras de Mensagens'


class Notificacao(models.Model):
    """
    Modelo para notificações do sistema.
    
    Representa uma notificação enviada a um usuário específico.
    Pode estar relacionada a diferentes tipos de objetos (tarefa, projeto, etc.)
    e ter diferentes níveis de prioridade. Rastreia se e quando a notificação foi lida.
    """
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
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notificacoes',
        help_text='Usuário que receberá a notificação'
    )
    tipo = models.CharField(
        max_length=20, 
        choices=TIPO_CHOICES,
        help_text='Tipo de objeto relacionado à notificação'
    )
    titulo = models.CharField(
        max_length=200,
        help_text='Título breve da notificação'
    )
    mensagem = models.TextField(help_text='Conteúdo detalhado da notificação')
    lida = models.BooleanField(
        default=False,
        help_text='Indica se a notificação foi lida pelo usuário'
    )
    prioridade = models.CharField(
        max_length=10, 
        choices=PRIORIDADE_CHOICES, 
        default='MEDIA',
        help_text='Nível de prioridade da notificação'
    )
    criada_em = models.DateTimeField(
        auto_now_add=True,
        help_text='Data e hora em que a notificação foi criada'
    )
    lida_em = models.DateTimeField(
        null=True, 
        blank=True,
        help_text='Data e hora em que a notificação foi lida (se aplicável)'
    )
    
    # Referências opcionais para objetos relacionados
    projeto = models.ForeignKey(
        Projeto, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text='Projeto relacionado à notificação (se aplicável)'
    )
    tarefa = models.ForeignKey(
        Tarefa, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text='Tarefa relacionada à notificação (se aplicável)'
    )
    url = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        help_text='URL para redirecionamento quando a notificação for clicada'
    )
    
    def clean(self):
        """Valida os campos do modelo antes de salvar."""
        super().clean()
        # Valida a URL se estiver presente
        if self.url:
            validator = URLValidator()
            try:
                validator(self.url)
            except ValidationError:
                raise ValidationError({'url': 'URL inválida. Forneça uma URL completa e válida.'})
    
    def __str__(self):
        return f"{self.get_tipo_display()}: {self.titulo} para {self.usuario.username}"  # type: ignore
    
    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-criada_em']


class ConfiguracaoNotificacao(models.Model):
    """
    Configurações de notificações por usuário.
    
    Armazena as preferências de cada usuário sobre como deseja receber
    notificações para diferentes tipos de eventos no sistema.
    Cada usuário tem exatamente uma configuração (garantido pela relação OneToOneField).
    """
    CANAL_CHOICES = (
        ('EMAIL', 'E-mail'),
        ('SISTEMA', 'Sistema'),
        ('AMBOS', 'Ambos'),
        ('NENHUM', 'Nenhum'),
    )
    
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='config_notificacoes',
        help_text='Usuário ao qual estas configurações pertencem'
    )
    
    # Configurações por tipo de evento
    tarefa_atribuida = models.CharField(
        max_length=10, 
        choices=CANAL_CHOICES, 
        default='AMBOS',
        help_text='Canal de notificação quando uma tarefa é atribuída ao usuário'
    )
    tarefa_comentario = models.CharField(
        max_length=10, 
        choices=CANAL_CHOICES, 
        default='SISTEMA',
        help_text='Canal de notificação quando há um novo comentário em uma tarefa do usuário'
    )
    tarefa_prazo = models.CharField(
        max_length=10, 
        choices=CANAL_CHOICES, 
        default='AMBOS',
        help_text='Canal de notificação para lembretes de prazo de tarefas'
    )
    projeto_status = models.CharField(
        max_length=10, 
        choices=CANAL_CHOICES, 
        default='SISTEMA',
        help_text='Canal de notificação quando o status de um projeto é alterado'
    )
    equipe_alteracao = models.CharField(
        max_length=10, 
        choices=CANAL_CHOICES, 
        default='SISTEMA',
        help_text='Canal de notificação quando há alterações na equipe de um projeto'
    )
    documento_novo = models.CharField(
        max_length=10, 
        choices=CANAL_CHOICES, 
        default='SISTEMA',
        help_text='Canal de notificação quando um novo documento é adicionado'
    )
    risco_novo = models.CharField(
        max_length=10, 
        choices=CANAL_CHOICES, 
        default='SISTEMA',
        help_text='Canal de notificação quando um novo risco é registrado'
    )
    mensagem_chat = models.CharField(
        max_length=10, 
        choices=CANAL_CHOICES, 
        default='SISTEMA',
        help_text='Canal de notificação para novas mensagens de chat'
    )
    
    def __str__(self):
        return f"Configurações de notificação para {self.usuario.username}"
    
    class Meta:
        verbose_name = 'Configuração de Notificação'
        verbose_name_plural = 'Configurações de Notificações'


class Comunicacao(models.Model):
    """
    Modelo para comunicações formais entre usuários em um projeto.
    
    Representa uma comunicação oficial enviada por um usuário para um ou mais
    destinatários no contexto de um projeto específico. Diferente das mensagens
    de chat, estas são mais estruturadas e formais.
    """
    TIPO_CHOICES = (
        ('ATA', 'Ata de Reunião'),
        ('MEMORANDO', 'Memorando'),
        ('RELATORIO', 'Relatório'),
        ('OFICIO', 'Ofício'),
        ('COMUNICADO', 'Comunicado Geral'),
        ('OUTRO', 'Outro'),
    )
    projeto = models.ForeignKey(
        Projeto, 
        on_delete=models.CASCADE, 
        related_name='comunicacoes',
        help_text='Projeto ao qual esta comunicação está associada'
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='OUTRO',
        help_text='Tipo de comunicação formal'
    )
    titulo = models.CharField(
        max_length=200,
        help_text='Título ou assunto da comunicação'
    )
    texto = models.TextField(help_text='Conteúdo detalhado da comunicação')
    remetente = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='comunicacoes_enviadas',
        help_text='Usuário que enviou a comunicação'
    )
    destinatarios = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='comunicacoes_recebidas',
        help_text='Usuários que receberam esta comunicação'
    )
    criada_em = models.DateTimeField(
        auto_now_add=True,
        help_text='Data e hora em que a comunicação foi criada'
    )
    atualizada_em = models.DateTimeField(
        auto_now=True,
        help_text='Data e hora da última atualização da comunicação'
    )
    
    class Meta:
        ordering = ['-criada_em']
        verbose_name = 'Comunicação'
        verbose_name_plural = 'Comunicações'
    
    def __str__(self):
        return self.titulo
