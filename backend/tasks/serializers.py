from rest_framework import serializers
from .models import Tarefa, AtribuicaoTarefa, ComentarioTarefa, HistoricoStatusTarefa
from users.serializers import UserSerializer


class ComentarioTarefaSerializer(serializers.ModelSerializer):
    autor_nome = serializers.CharField(source='autor.full_name', read_only=True)
    
    class Meta:
        model = ComentarioTarefa
        fields = ['id', 'tarefa', 'autor', 'autor_nome', 'texto', 'criado_em']
        read_only_fields = ['criado_em']


class HistoricoStatusTarefaSerializer(serializers.ModelSerializer):
    alterado_por_nome = serializers.CharField(source='alterado_por.full_name', read_only=True)
    status_anterior_display = serializers.CharField(source='get_status_anterior_display', read_only=True)
    novo_status_display = serializers.CharField(source='get_novo_status_display', read_only=True)
    
    class Meta:
        model = HistoricoStatusTarefa
        fields = ['id', 'tarefa', 'status_anterior', 'status_anterior_display', 
                  'novo_status', 'novo_status_display', 'alterado_por', 
                  'alterado_por_nome', 'alterado_em']
        read_only_fields = ['alterado_em']


class AtribuicaoTarefaSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.full_name', read_only=True)
    atribuido_por_nome = serializers.CharField(source='atribuido_por.full_name', read_only=True)
    
    class Meta:
        model = AtribuicaoTarefa
        fields = ['id', 'tarefa', 'usuario', 'usuario_nome', 
                  'atribuido_em', 'atribuido_por', 'atribuido_por_nome']
        read_only_fields = ['atribuido_em']


class TarefaSerializer(serializers.ModelSerializer):
    criado_por = UserSerializer(read_only=True)
    atribuicoes = serializers.SerializerMethodField()
    
    class Meta:
        model = Tarefa
        fields = [
            'id', 'titulo', 'descricao', 'projeto', 'sprint',
            'data_inicio', 'data_termino', 'prioridade', 'status',
            'criado_por', 'criado_em', 'atualizado_em', 'atribuicoes'
        ]
        read_only_fields = ['criado_por', 'criado_em', 'atualizado_em']
    
    def get_atribuicoes(self, obj):
        return AtribuicaoTarefaSerializer(obj.atribuicoes.all(), many=True).data

class TarefaListSerializer(serializers.ModelSerializer):
    criado_por = UserSerializer(read_only=True)
    atribuicoes = AtribuicaoTarefaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Tarefa
        fields = [
            'id', 'titulo', 'projeto', 'sprint', 'status',
            'prioridade', 'data_termino', 'criado_por', 'atribuicoes'
        ]

class AtribuicaoTarefaSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    atribuido_por = UserSerializer(read_only=True)
    
    class Meta:
        model = AtribuicaoTarefa
        fields = ['id', 'tarefa', 'usuario', 'atribuido_em', 'atribuido_por']
        read_only_fields = ['atribuido_em', 'atribuido_por']

class ComentarioTarefaSerializer(serializers.ModelSerializer):
    autor = UserSerializer(read_only=True)
    
    class Meta:
        model = ComentarioTarefa
        fields = ['id', 'tarefa', 'autor', 'texto', 'criado_em']
        read_only_fields = ['criado_em', 'autor']

class HistoricoStatusTarefaSerializer(serializers.ModelSerializer):
    alterado_por = UserSerializer(read_only=True)
    
    class Meta:
        model = HistoricoStatusTarefa
        fields = ['id', 'tarefa', 'status_anterior', 'novo_status', 'alterado_por', 'alterado_em']
        read_only_fields = ['alterado_em']
