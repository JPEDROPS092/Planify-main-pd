"""
Definição dos modelos de dados para o sistema de gerenciamento de custos.
Inclui modelos para Categorias de Custo, Custos, Orçamentos de Projeto,
Orçamentos de Tarefa e Alertas de Orçamento.
"""
from django.db import models
from django.conf import settings
from projects.models import Projeto
from tasks.models import Tarefa
from decimal import Decimal
from django.db.models import Sum

class Categoria(models.Model):
    """Categoria de custos para classificação"""
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']


class Custo(models.Model):
    """Registro de custos associados a projetos e opcionalmente a tarefas"""
    TIPO_CHOICES = (
        ('FIXO', 'Custo Fixo'),
        ('VARIAVEL', 'Custo Variável'),
        ('RECORRENTE', 'Custo Recorrente'),
    )
    
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='custos')
    tarefa = models.ForeignKey(
        Tarefa, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='custos'
    )
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='custos'
    )
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='FIXO')
    data = models.DateField()
    comprovante = models.FileField(upload_to='comprovantes/', blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='custos_registrados'
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"
    
    class Meta:
        verbose_name = 'Custo'
        verbose_name_plural = 'Custos'
        ordering = ['-data']


class OrcamentoProjeto(models.Model):
    """Orçamento planejado para um projeto"""
    projeto = models.OneToOneField(Projeto, on_delete=models.CASCADE, related_name='orcamento')
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    data_aprovacao = models.DateField(auto_now_add=True)
    aprovado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orcamentos_aprovados'
    )
    observacoes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Orçamento de {self.projeto.titulo} - R$ {self.valor_total}"
    
    class Meta:
        verbose_name = 'Orçamento de Projeto'
        verbose_name_plural = 'Orçamentos de Projetos'


class OrcamentoTarefa(models.Model):
    """Orçamento planejado para uma tarefa específica"""
    tarefa = models.OneToOneField(Tarefa, on_delete=models.CASCADE, related_name='orcamento')
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data_aprovacao = models.DateField(auto_now_add=True)
    aprovado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orcamentos_tarefa_aprovados'
    )
    observacoes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Orçamento para {self.tarefa.titulo} - R$ {self.valor}"
    
    # Os campos valor_utilizado, valor_restante e percentual_utilizado
    # serão calculados diretamente na query via anotações no ViewSet
    
    class Meta:
        verbose_name = 'Orçamento de Tarefa'
        verbose_name_plural = 'Orçamentos de Tarefas'


class Alerta(models.Model):
    """Alertas de orçamento quando o gasto atinge determinado percentual"""
    TIPO_CHOICES = (
        ('PROJETO', 'Projeto'),
        ('TAREFA', 'Tarefa'),
    )
    
    STATUS_CHOICES = (
        ('ATIVO', 'Ativo'),
        ('RESOLVIDO', 'Resolvido'),
        ('IGNORADO', 'Ignorado'),
    )
    
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='alertas')
    tarefa = models.ForeignKey(
        Tarefa, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='alertas'
    )
    percentual = models.DecimalField(max_digits=5, decimal_places=2)
    mensagem = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ATIVO')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_resolucao = models.DateTimeField(null=True, blank=True)
    resolvido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='alertas_resolvidos'
    )
    
    def __str__(self):
        if self.tipo == 'PROJETO':
            return f"Alerta de {self.percentual}% para {self.projeto.titulo}"
        return f"Alerta de {self.percentual}% para {self.tarefa.titulo}" if self.tarefa else f"Alerta de {self.percentual}% para projeto"
    
    class Meta:
        verbose_name = 'Alerta de Orçamento'
        verbose_name_plural = 'Alertas de Orçamento'
        ordering = ['-data_criacao']
