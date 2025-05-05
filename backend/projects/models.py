from django.db import models
from django.conf import settings
from django.utils import timezone


class Projeto(models.Model):
    STATUS_CHOICES = (
        ('PLANEJADO', 'Planejado'),
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('PAUSADO', 'Pausado'),
        ('CONCLUIDO', 'Concluído'),
        ('CANCELADO', 'Cancelado'),
    )
    
    PRIORIDADE_CHOICES = (
        ('BAIXA', 'Baixa'),
        ('MEDIA', 'Média'),
        ('ALTA', 'Alta'),
    )
    
    titulo = models.CharField(max_length=100, unique=True)
    descricao = models.TextField()
    data_inicio = models.DateField()
    data_fim = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANEJADO')
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default='MEDIA')
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True,
        related_name='projetos_criados'
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    arquivado = models.BooleanField(default=False)
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'


class MembroProjeto(models.Model):
    PAPEL_CHOICES = (
        ('GERENTE', 'Gerente de Projeto'),
        ('DESENVOLVEDOR', 'Desenvolvedor'),
        ('TESTADOR', 'Testador'),
        ('ANALISTA', 'Analista'),
        ('DESIGNER', 'Designer'),
    )
    
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='membros')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participacoes_projeto')
    papel = models.CharField(max_length=20, choices=PAPEL_CHOICES)
    data_entrada = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('projeto', 'usuario')
        verbose_name = 'Membro do Projeto'
        verbose_name_plural = 'Membros do Projeto'
    
    def __str__(self):
        return f"{self.usuario.username} - {self.projeto.titulo} ({self.get_papel_display()})"


class HistoricoStatusProjeto(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='historico_status')
    status_anterior = models.CharField(max_length=20, choices=Projeto.STATUS_CHOICES)
    novo_status = models.CharField(max_length=20, choices=Projeto.STATUS_CHOICES)
    alterado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    alterado_em = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-alterado_em']
        verbose_name = 'Histórico de Status'
        verbose_name_plural = 'Históricos de Status'
    
    def __str__(self):
        return f"{self.projeto.titulo}: {self.status_anterior} -> {self.novo_status} ({self.alterado_em})"


class Sprint(models.Model):
    STATUS_CHOICES = (
        ('PLANEJADO', 'Planejado'),
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('CONCLUIDO', 'Concluído'),
        ('CANCELADO', 'Cancelado'),
    )
    
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='sprints', null=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANEJADO')
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('projeto', 'nome')
        ordering = ['data_inicio']
        verbose_name = 'Sprint'
        verbose_name_plural = 'Sprints'
    
    def __str__(self):
        return f"{self.projeto.titulo} - {self.nome}"
