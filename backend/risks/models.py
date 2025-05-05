from django.db import models
from django.conf import settings
from projects.models import Projeto


class Risco(models.Model):
    PROBABILIDADE_CHOICES = (
        ('BAIXA', 'Baixa'),
        ('MEDIA', 'Média'),
        ('ALTA', 'Alta'),
    )
    
    IMPACTO_CHOICES = (
        ('BAIXO', 'Baixo'),
        ('MEDIO', 'Médio'),
        ('ALTO', 'Alto'),
    )
    
    STATUS_CHOICES = (
        ('IDENTIFICADO', 'Identificado'),
        ('EM_ANALISE', 'Em Análise'),
        ('MITIGADO', 'Mitigado'),
        ('ACEITO', 'Aceito'),
        ('ELIMINADO', 'Eliminado'),
    )
    
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='riscos')
    descricao = models.TextField()
    probabilidade = models.CharField(max_length=10, choices=PROBABILIDADE_CHOICES)
    impacto = models.CharField(max_length=10, choices=IMPACTO_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IDENTIFICADO')
    responsavel_mitigacao = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='riscos_responsavel'
    )
    plano_mitigacao = models.TextField(blank=True, null=True)
    plano_contingencia = models.TextField(blank=True, null=True)
    data_identificacao = models.DateField(auto_now_add=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='riscos_criados'
    )
    atualizado_em = models.DateTimeField(auto_now=True)
    
    @property
    def nivel_risco(self):
        """
        Calcula o nível de risco com base na probabilidade e impacto.
        Retorna: BAIXO, MEDIO ou ALTO
        """
        matriz_risco = {
            # probabilidade x impacto = nível de risco
            ('BAIXA', 'BAIXO'): 'BAIXO',
            ('BAIXA', 'MEDIO'): 'BAIXO',
            ('BAIXA', 'ALTO'): 'MEDIO',
            ('MEDIA', 'BAIXO'): 'BAIXO',
            ('MEDIA', 'MEDIO'): 'MEDIO',
            ('MEDIA', 'ALTO'): 'ALTO',
            ('ALTA', 'BAIXO'): 'MEDIO',
            ('ALTA', 'MEDIO'): 'ALTO',
            ('ALTA', 'ALTO'): 'ALTO',
        }
        return matriz_risco.get((self.probabilidade, self.impacto), 'MEDIO')
    
    def __str__(self):
        return f"Risco: {self.descricao[:50]}... ({self.get_status_display()})"
    
    class Meta:
        verbose_name = 'Risco'
        verbose_name_plural = 'Riscos'
        ordering = ['-data_identificacao']


class HistoricoRisco(models.Model):
    risco = models.ForeignKey(Risco, on_delete=models.CASCADE, related_name='historico')
    status_anterior = models.CharField(max_length=20, choices=Risco.STATUS_CHOICES)
    novo_status = models.CharField(max_length=20, choices=Risco.STATUS_CHOICES)
    probabilidade_anterior = models.CharField(max_length=10, choices=Risco.PROBABILIDADE_CHOICES)
    nova_probabilidade = models.CharField(max_length=10, choices=Risco.PROBABILIDADE_CHOICES)
    impacto_anterior = models.CharField(max_length=10, choices=Risco.IMPACTO_CHOICES)
    novo_impacto = models.CharField(max_length=10, choices=Risco.IMPACTO_CHOICES)
    alterado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    alterado_em = models.DateTimeField(auto_now_add=True)
    observacao = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Histórico de Risco'
        verbose_name_plural = 'Históricos de Riscos'
        ordering = ['-alterado_em']
    
    def __str__(self):
        return f"Alteração em {self.risco} - {self.alterado_em.strftime('%d/%m/%Y %H:%M')}"
