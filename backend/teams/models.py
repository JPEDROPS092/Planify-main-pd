from django.db import models
from django.conf import settings


class Equipe(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='equipes_criadas'
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Equipe'
        verbose_name_plural = 'Equipes'
        ordering = ['nome']


class MembroEquipe(models.Model):
    PAPEL_CHOICES = (
        ('PO', 'Product Owner'),
        ('SM', 'Scrum Master'),
        ('DEV', 'Desenvolvedor'),
        ('QA', 'Analista de Qualidade'),
        ('DESIGN', 'Designer'),
        ('ANALISTA', 'Analista'),
    )
    
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, related_name='membros')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='equipes')
    papel = models.CharField(max_length=20, choices=PAPEL_CHOICES)
    adicionado_em = models.DateTimeField(auto_now_add=True)
    adicionado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='membros_adicionados'
    )
    
    class Meta:
        unique_together = ('equipe', 'usuario')
        verbose_name = 'Membro da Equipe'
        verbose_name_plural = 'Membros da Equipe'
    
    def get_papel_display(self):
        return dict(self.PAPEL_CHOICES).get(self.papel, self.papel)

    def __str__(self):
        return f"{self.usuario.username} - {self.equipe.nome} ({self.get_papel_display()})"
    
    def save(self, *args, **kwargs):
        # Se este é o primeiro membro da equipe e não tem papel definido, 
        # define como PO (Product Owner)
        if not self.pk and not MembroEquipe.objects.filter(equipe=self.equipe).exists() and not self.papel:
            self.papel = 'PO'
        super().save(*args, **kwargs)


class PermissaoEquipe(models.Model):
    PERMISSAO_CHOICES = (
        ('VISUALIZAR', 'Visualizar'),
        ('CRIAR', 'Criar'),
        ('EDITAR', 'Editar'),
        ('EXCLUIR', 'Excluir'),
    )
    
    MODULO_CHOICES = (
        ('TAREFAS', 'Tarefas'),
        ('SPRINTS', 'Sprints'),
        ('DOCUMENTOS', 'Documentos'),
        ('RISCOS', 'Riscos'),
        ('CUSTOS', 'Custos'),
    )
    
    papel = models.CharField(max_length=20, choices=MembroEquipe.PAPEL_CHOICES)
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, related_name='permissoes')
    modulo = models.CharField(max_length=20, choices=MODULO_CHOICES)
    permissao = models.CharField(max_length=20, choices=PERMISSAO_CHOICES)
    
    class Meta:
        unique_together = ('papel', 'equipe', 'modulo', 'permissao')
        verbose_name = 'Permissão de Equipe'
        verbose_name_plural = 'Permissões de Equipe'
    
    def __str__(self):
            return f"{self.equipe.nome} - {self.get_papel_display()} - {self.get_modulo_display()} - {self.get_permissao_display()}"
    
    def get_papel_display(self):
            return dict(MembroEquipe.PAPEL_CHOICES).get(self.papel, self.papel)
        
    def get_modulo_display(self):
            return dict(self.MODULO_CHOICES).get(self.modulo, self.modulo)
        
    def get_permissao_display(self):
            return dict(self.PERMISSAO_CHOICES).get(self.permissao, self.permissao)
