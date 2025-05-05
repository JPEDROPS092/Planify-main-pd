from rest_framework import serializers
from .models import Projeto, MembroProjeto, Sprint, HistoricoStatusProjeto
from tasks.models import Tarefa


class MembroProjetoSerializer(serializers.ModelSerializer):
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    username = serializers.CharField(source='usuario.username', read_only=True)
    full_name = serializers.CharField(source='usuario.get_full_name', read_only=True)
    
    class Meta:
        model = MembroProjeto
        fields = ['id', 'usuario', 'usuario_id', 'username', 'full_name', 'papel', 'data_entrada']
        extra_kwargs = {
            'usuario': {'write_only': True}
        }


class SprintSerializer(serializers.ModelSerializer):
    tasks_count = serializers.SerializerMethodField()
    completed_tasks_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Sprint
        fields = ['id', 'projeto', 'nome', 'descricao', 'data_inicio', 'data_fim', 
                 'status', 'criado_por', 'criado_em', 'tasks_count', 'completed_tasks_count']
        read_only_fields = ['criado_por', 'criado_em']
    
    def get_tasks_count(self, obj):
        return Tarefa.objects.filter(sprint=obj).count()
    
    def get_completed_tasks_count(self, obj):
        return Tarefa.objects.filter(sprint=obj, status='FEITO').count()


class ProjetoSerializer(serializers.ModelSerializer):
    membros = MembroProjetoSerializer(many=True, read_only=True)
    sprints_count = serializers.SerializerMethodField()
    tasks_count = serializers.SerializerMethodField()
    progresso = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    prioridade_display = serializers.CharField(source='get_prioridade_display', read_only=True)
    
    class Meta:
        model = Projeto
        fields = ['id', 'titulo', 'descricao', 'data_inicio', 'data_fim', 'status', 
                 'status_display', 'prioridade', 'prioridade_display', 'criado_por', 
                 'criado_em', 'atualizado_em', 'arquivado', 'membros', 
                 'sprints_count', 'tasks_count', 'progresso']
        read_only_fields = ['criado_por', 'criado_em', 'atualizado_em']
    
    def get_sprints_count(self, obj):
        return obj.sprints.count()
    
    def get_tasks_count(self, obj):
        return Tarefa.objects.filter(projeto=obj).count()
    
    def get_progresso(self, obj):
        tasks = Tarefa.objects.filter(projeto=obj)
        total_tasks = tasks.count()
        
        if total_tasks == 0:
            return 0
        
        completed_tasks = tasks.filter(status='FEITO').count()
        return int((completed_tasks / total_tasks) * 100)


class ProjetoListSerializer(serializers.ModelSerializer):
    membros_count = serializers.SerializerMethodField()
    tasks_count = serializers.SerializerMethodField()
    progresso = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    prioridade_display = serializers.CharField(source='get_prioridade_display', read_only=True)
    
    class Meta:
        model = Projeto
        fields = ['id', 'titulo', 'descricao', 'data_inicio', 'data_fim', 'status', 
                 'status_display', 'prioridade', 'prioridade_display', 'criado_em', 
                 'atualizado_em', 'arquivado', 'membros_count', 'tasks_count', 'progresso']
    
    def get_membros_count(self, obj):
        return obj.membros.count()
    
    def get_tasks_count(self, obj):
        return Tarefa.objects.filter(projeto=obj).count()
    
    def get_progresso(self, obj):
        tasks = Tarefa.objects.filter(projeto=obj)
        total_tasks = tasks.count()
        
        if total_tasks == 0:
            return 0
        
        completed_tasks = tasks.filter(status='FEITO').count()
        return int((completed_tasks / total_tasks) * 100)


class HistoricoStatusProjetoSerializer(serializers.ModelSerializer):
    status_anterior_display = serializers.CharField(source='get_status_anterior_display', read_only=True)
    novo_status_display = serializers.CharField(source='get_novo_status_display', read_only=True)
    
    class Meta:
        model = HistoricoStatusProjeto
        fields = ['id', 'projeto', 'status_anterior', 'status_anterior_display', 
                 'novo_status', 'novo_status_display', 'alterado_por', 'alterado_em']
        read_only_fields = ['alterado_em']
