from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from drf_spectacular.utils import extend_schema_field, extend_schema_serializer
from drf_spectacular.types import OpenApiTypes
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import Projeto, MembroProjeto, Sprint, HistoricoStatusProjeto
from tasks.models import Tarefa

User = get_user_model()


# Documentação do serializer está no docstring da classe
class MembroProjetoSerializer(serializers.ModelSerializer):
    """Serializer para membros de projeto.
    
    Inclui informações básicas do usuário e seu papel no projeto.
    """
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    username = serializers.CharField(source='usuario.username', read_only=True)
    full_name = serializers.CharField(source='usuario.full_name', read_only=True)
    papel_display = serializers.CharField(source='get_papel_display', read_only=True, help_text="Nome do papel para exibição")
    
    class Meta:
        model = MembroProjeto
        fields = ['id', 'usuario', 'usuario_id', 'username', 'full_name', 'papel', 'papel_display', 'data_entrada']
        extra_kwargs = {
            'usuario': {'write_only': True},
            'data_entrada': {'read_only': True}
        }
        validators = [
            UniqueTogetherValidator(
                queryset=MembroProjeto.objects.all(),
                fields=['projeto', 'usuario'],
                message=_('Este usuário já é membro deste projeto.')
            )
        ]
    
    def validate_papel(self, value):
        """Valida se o papel fornecido é válido."""
        valid_roles = dict(MembroProjeto.PAPEL_CHOICES).keys()
        if value not in valid_roles:
            raise serializers.ValidationError(
                _('Papel inválido. Escolha entre: {}').format(", ".join(valid_roles))
            )
        return value


# Documentação do serializer está no docstring da classe
class SprintSerializer(serializers.ModelSerializer):
    """Serializer para sprints.
    
    Inclui informações básicas da sprint e estatísticas de tarefas.
    """
    # Contagem de tarefas associadas a esta sprint
    tasks_count = serializers.SerializerMethodField(help_text="Número total de tarefas nesta sprint")
    # Contagem de tarefas concluídas nesta sprint
    completed_tasks_count = serializers.SerializerMethodField(help_text="Número de tarefas concluídas nesta sprint")
    # Representação textual do status
    status_display = serializers.CharField(source='get_status_display', read_only=True, help_text="Nome do status para exibição")
    # Nome do projeto para exibição
    projeto_nome = serializers.CharField(source='projeto.titulo', read_only=True, help_text="Nome do projeto")
    # Progresso da sprint
    progresso = serializers.SerializerMethodField(help_text="Progresso da sprint em percentual (0-100)")
    
    class Meta:
        model = Sprint
        fields = ['id', 'projeto', 'projeto_nome', 'nome', 'descricao', 'data_inicio', 'data_fim', 
                 'status', 'status_display', 'criado_por', 'criado_em', 'tasks_count', 
                 'completed_tasks_count', 'progresso']
        read_only_fields = ['criado_por', 'criado_em']
    
    def validate(self, data):
        """Validação personalizada para garantir que a data de início seja anterior à data de fim."""
        if 'data_inicio' in data and 'data_fim' in data:
            if data['data_inicio'] > data['data_fim']:
                raise serializers.ValidationError({
                    'data_fim': _('A data de fim deve ser posterior à data de início.')
                })
        return data
    
    def validate_projeto(self, value):
        """Valida se o usuário tem acesso ao projeto."""
        user = self.context['request'].user
        if not MembroProjeto.objects.filter(projeto=value, usuario=user).exists():
            raise serializers.ValidationError(_('Você não tem permissão para criar sprints neste projeto.'))
        return value
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_tasks_count(self, obj):
        """Retorna o número total de tarefas vinculadas à sprint."""
        return Tarefa.objects.filter(sprint=obj).count()
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_completed_tasks_count(self, obj):
        """Retorna o número de tarefas marcadas como 'FEITO' (concluídas) na sprint."""
        return Tarefa.objects.filter(sprint=obj, status='FEITO').count()
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_progresso(self, obj):
        """Calcula o progresso da sprint como a porcentagem de tarefas concluídas."""
        tasks = Tarefa.objects.filter(sprint=obj)
        total_tasks = tasks.count()
        
        if total_tasks == 0:
            return 0
        
        completed_tasks = tasks.filter(status='FEITO').count()
        return int((completed_tasks / total_tasks) * 100)


# Documentação do serializer está no docstring da classe
class ProjetoSerializer(serializers.ModelSerializer):
    """Serializer completo para projetos.
    
    Inclui informações detalhadas do projeto, membros, estatísticas de sprints e tarefas.
    """
    membros = MembroProjetoSerializer(many=True, read_only=True, help_text="Lista de membros associados ao projeto")
    # Contagem de sprints no projeto
    sprints_count = serializers.SerializerMethodField(help_text="Número total de sprints neste projeto")
    # Contagem de tarefas no projeto
    tasks_count = serializers.SerializerMethodField(help_text="Número total de tarefas neste projeto")
    # Progresso do projeto em percentual
    progresso = serializers.SerializerMethodField(help_text="Progresso do projeto em percentual (0-100)")
    # Representações textuais
    status_display = serializers.CharField(source='get_status_display', read_only=True, help_text="Nome do status para exibição")
    prioridade_display = serializers.CharField(source='get_prioridade_display', read_only=True, help_text="Nome da prioridade para exibição")
    # Informações do criador
    criador_username = serializers.CharField(source='criado_por.username', read_only=True, help_text="Nome de usuário do criador")
    criador_nome = serializers.CharField(source='criado_por.full_name', read_only=True, help_text="Nome completo do criador")
    # Estatísticas adicionais
    dias_restantes = serializers.SerializerMethodField(help_text="Dias restantes até a data de fim")
    atrasado = serializers.SerializerMethodField(help_text="Indica se o projeto está atrasado")
    
    class Meta:
        model = Projeto
        fields = ['id', 'titulo', 'descricao', 'data_inicio', 'data_fim', 'status', 
                 'status_display', 'prioridade', 'prioridade_display', 'criado_por', 
                 'criador_username', 'criador_nome', 'criado_em', 'atualizado_em', 
                 'arquivado', 'membros', 'sprints_count', 'tasks_count', 'progresso',
                 'dias_restantes', 'atrasado']
        read_only_fields = ['criado_por', 'criado_em', 'atualizado_em']
    
    def validate(self, data):
        """Validação personalizada para garantir que a data de início seja anterior à data de fim."""
        if 'data_inicio' in data and 'data_fim' in data:
            if data['data_inicio'] > data['data_fim']:
                raise serializers.ValidationError({
                    'data_fim': _('A data de fim deve ser posterior à data de início.')
                })
        return data
    
    def validate_titulo(self, value):
        """Valida se o título é único."""
        instance = getattr(self, 'instance', None)
        if instance:
            # Se estamos atualizando, verificamos se o título já existe para outro projeto
            if Projeto.objects.exclude(pk=instance.pk).filter(titulo=value).exists():
                raise serializers.ValidationError(_('Já existe um projeto com este título.'))
        else:
            # Se estamos criando, verificamos se o título já existe
            if Projeto.objects.filter(titulo=value).exists():
                raise serializers.ValidationError(_('Já existe um projeto com este título.'))
        return value
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_sprints_count(self, obj):
        """Retorna o número de sprints associadas diretamente ao projeto."""
        return obj.sprints.count()
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_tasks_count(self, obj):
        """Retorna o número total de tarefas vinculadas ao projeto."""
        return Tarefa.objects.filter(projeto=obj).count()
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_progresso(self, obj):
        """Calcula o progresso do projeto como a porcentagem de tarefas concluídas."""
        tasks = Tarefa.objects.filter(projeto=obj)
        total_tasks = tasks.count()
        
        if total_tasks == 0:
            return 0
        
        completed_tasks = tasks.filter(status='FEITO').count()
        return int((completed_tasks / total_tasks) * 100)
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_dias_restantes(self, obj):
        """Calcula os dias restantes até a data de fim do projeto."""
        from django.utils import timezone
        import datetime
        
        hoje = timezone.now().date()
        if obj.data_fim < hoje:
            return 0
        return (obj.data_fim - hoje).days
    
    @extend_schema_field(OpenApiTypes.BOOL)
    def get_atrasado(self, obj):
        """Verifica se o projeto está atrasado (data de fim já passou e não está concluído)."""
        from django.utils import timezone
        
        hoje = timezone.now().date()
        return obj.data_fim < hoje and obj.status != 'CONCLUIDO'


# Documentação do serializer está no docstring da classe
class ProjetoListSerializer(serializers.ModelSerializer):
    """Serializer otimizado para listagem de projetos.
    
    Inclui informações resumidas e estatísticas básicas para listagem eficiente.
    """
    # Contagem de membros no projeto
    membros_count = serializers.SerializerMethodField(help_text="Número total de membros neste projeto")
    # Contagem de tarefas no projeto
    tasks_count = serializers.SerializerMethodField(help_text="Número total de tarefas neste projeto")
    # Progresso do projeto em percentual
    progresso = serializers.SerializerMethodField(help_text="Progresso do projeto em percentual (0-100)")
    # Representações textuais
    status_display = serializers.CharField(source='get_status_display', read_only=True, help_text="Nome do status para exibição")
    prioridade_display = serializers.CharField(source='get_prioridade_display', read_only=True, help_text="Nome da prioridade para exibição")
    # Informações do criador
    criador_username = serializers.CharField(source='criado_por.username', read_only=True, help_text="Nome de usuário do criador")
    # Estatísticas adicionais
    atrasado = serializers.SerializerMethodField(help_text="Indica se o projeto está atrasado")
    
    class Meta:
        model = Projeto
        fields = ['id', 'titulo', 'descricao', 'data_inicio', 'data_fim', 'status', 
                 'status_display', 'prioridade', 'prioridade_display', 'criado_em', 
                 'atualizado_em', 'arquivado', 'membros_count', 'tasks_count', 'progresso',
                 'criador_username', 'atrasado']
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_membros_count(self, obj):
        """Retorna o número de membros associados ao projeto."""
        return obj.membros.count()
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_tasks_count(self, obj):
        """Retorna o número total de tarefas vinculadas ao projeto."""
        return Tarefa.objects.filter(projeto=obj).count()
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_progresso(self, obj):
        """Calcula o progresso do projeto como a porcentagem de tarefas concluídas."""
        tasks = Tarefa.objects.filter(projeto=obj)
        total_tasks = tasks.count()
        
        if total_tasks == 0:
            return 0
        
        completed_tasks = tasks.filter(status='FEITO').count()
        return int((completed_tasks / total_tasks) * 100)
    
    @extend_schema_field(OpenApiTypes.BOOL)
    def get_atrasado(self, obj):
        """Verifica se o projeto está atrasado (data de fim já passou e não está concluído)."""
        from django.utils import timezone
        
        hoje = timezone.now().date()
        return obj.data_fim < hoje and obj.status != 'CONCLUIDO'


# Documentação do serializer está no docstring da classe
class HistoricoStatusProjetoSerializer(serializers.ModelSerializer):
    """Serializer para histórico de alterações de status de projeto.
    
    Registra as mudanças de status com informações sobre quem e quando alterou.
    """
    status_anterior_display = serializers.CharField(source='get_status_anterior_display', read_only=True, help_text="Nome do status anterior para exibição")
    alterado_por_username = serializers.CharField(source='alterado_por.username', read_only=True, help_text="Nome de usuário de quem alterou o status")
    projeto_titulo = serializers.CharField(source='projeto.titulo', read_only=True, help_text="Título do projeto")
    
    class Meta:
        model = HistoricoStatusProjeto
        fields = ['id', 'projeto', 'projeto_titulo', 'status_anterior', 'status_anterior_display', 
                 'alterado_por', 'alterado_por_username', 'alterado_em']
        read_only_fields = ['alterado_em']
    
    def validate(self, data):
        """Validação personalizada para o histórico de status."""
        return data
    

