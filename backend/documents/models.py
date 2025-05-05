from django.db import models
from django.conf import settings
from projects.models import Projeto
from tasks.models import Tarefa


class Documento(models.Model):
    """Modelo para armazenar documentos associados a projetos e tarefas"""
    TIPO_CHOICES = (
        ('REQUISITO', 'Requisito'),
        ('DESIGN', 'Design'),
        ('MANUAL', 'Manual'),
        ('RELATORIO', 'Relatório'),
        ('ATA', 'Ata de Reunião'),
        ('OUTRO', 'Outro'),
    )
    
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='documentos')
    tarefa = models.ForeignKey(
        Tarefa, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='documentos'
    )
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='OUTRO')
    arquivo = models.FileField(upload_to='documentos/')
    tamanho_arquivo = models.PositiveIntegerField(help_text='Tamanho em bytes')
    tipo_arquivo = models.CharField(max_length=50, help_text='Tipo MIME do arquivo')
    versao = models.CharField(max_length=20, default='1.0')
    enviado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='documentos_enviados'
    )
    data_upload = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.titulo} - {self.get_tipo_display()} (v{self.versao})"
    
    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['-data_upload']


class HistoricoDocumento(models.Model):
    """Histórico de versões de documentos"""
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='historico')
    versao_anterior = models.CharField(max_length=20)
    arquivo_anterior = models.FileField(upload_to='documentos/historico/')
    tamanho_arquivo = models.PositiveIntegerField(help_text='Tamanho em bytes')
    alterado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    data_alteracao = models.DateTimeField(auto_now_add=True)
    observacao = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.documento.titulo} - v{self.versao_anterior}"
    
    class Meta:
        verbose_name = 'Histórico de Documento'
        verbose_name_plural = 'Históricos de Documentos'
        ordering = ['-data_alteracao']


class Comentario(models.Model):
    """Comentários em documentos"""
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comentário em {self.documento.titulo} por {self.autor.username}"
    
    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['-criado_em']
