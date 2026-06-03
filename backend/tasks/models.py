from django.db import models
from django.conf import settings
from projects.models import Projeto, Sprint

from customers.managers import TenantManager


class Tarefa(models.Model):
    STATUS_CHOICES = (
        ('A_FAZER', 'A Fazer'),
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('FEITO', 'Feito'),
    )
    
    PRIORITY_CHOICES = (
        ('BAIXA', 'Baixa'),
        ('MEDIA', 'Média'),
        ('ALTA', 'Alta'),
    )
    
    tenant = models.ForeignKey(
        'customers.Client',
        on_delete=models.CASCADE,
        related_name='+',
    )
    objects = TenantManager()
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_inicio = models.DateField()
    data_termino = models.DateField()
    prioridade = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIA')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='A_FAZER')
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='tarefas')
    sprint = models.ForeignKey(Sprint, on_delete=models.SET_NULL, null=True, blank=True, related_name='tarefas')
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True,
        related_name='tarefas_criadas'
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    atualizado_por = models.ForeignKey  (settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='tarefas_atualizadas'
    )
    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering = ['prioridade', 'data_termino']
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'
        indexes = [
            models.Index(fields=['tenant', 'prioridade', 'data_termino']),
        ]


class AtribuicaoTarefa(models.Model):
    tenant = models.ForeignKey(
        'customers.Client',
        on_delete=models.CASCADE,
        related_name='+',
    )
    objects = TenantManager()
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name='atribuicoes')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tarefas_atribuidas')
    atribuido_em = models.DateTimeField(auto_now_add=True)
    atribuido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True,
        related_name='atribuicoes_feitas'
    )
    
    class Meta:
        unique_together = ('tarefa', 'usuario')
        verbose_name = 'Atribuição de Tarefa'
        verbose_name_plural = 'Atribuições de Tarefas'
    
    def __str__(self):
        return f"{self.tarefa.titulo} - {self.usuario.username}"


class ComentarioTarefa(models.Model):
    tenant = models.ForeignKey(
        'customers.Client',
        on_delete=models.CASCADE,
        related_name='+',
    )
    objects = TenantManager()
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        indexes = [
            models.Index(fields=['tenant', '-criado_em']),
        ]
    
    def __str__(self):
        return f"Comentário de {self.autor.username} em {self.tarefa.titulo}"


class HistoricoStatusTarefa(models.Model):
    tenant = models.ForeignKey(
        'customers.Client',
        on_delete=models.CASCADE,
        related_name='+',
    )
    objects = TenantManager()
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name='historico_status')
    status_anterior = models.CharField(max_length=20, choices=Tarefa.STATUS_CHOICES)
    novo_status = models.CharField(max_length=20, choices=Tarefa.STATUS_CHOICES)
    alterado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    alterado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-alterado_em']
        verbose_name = 'Histórico de Status'
        verbose_name_plural = 'Históricos de Status'
        indexes = [
            models.Index(fields=['tenant', '-alterado_em']),
        ]

    def __str__(self):
        return f"{self.tarefa.titulo}: {self.status_anterior} -> {self.novo_status}"
